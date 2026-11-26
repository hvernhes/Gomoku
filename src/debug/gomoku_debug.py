"""Visual debug tool for the search (V2).

Usage, from the repository root (virtual environment activated):

    python3 -m src.debug.gomoku_debug [game_log]

See README.md in this folder for the full explanation. In short: an analysis
board where you load a game log (or start empty), move through the game,
analyse the displayed position (key A), then walk down the recorded search
tree with the mouse. For the displayed node the board shows the candidate
cells (green border), the score of every move the search tried, the moves it
cut (grey dot) and the illegal candidates (red cross); hovering a move draws
the line of play the search expects after it.
"""
import math
import re
import sys
from dataclasses import dataclass, field

import pygame

from board import (
    BLACK,
    EMPTY,
    STONE_RADIUS,
    WHITE
)
from src.ai.candidates import (
    CANDIDATE_RADIUS,
    candidate_cells
)
from src.ai.minimax import WIN_SCORE
from src.ai.weights import (
    HeuristicWeights,
    generate_weights
)
from src.debug.recorder import (
    Analysis,
    analyse,
    bound_kind,
    find_node,
    is_maximizing,
    principal_line
)
from src.game.Board import Board
from src.game.Cell import Cell
from src.helpers.computation import (
    compute_forbidden,
    compute_result,
    intersection_to_pixel,
    pixel_to_intersection
)
from src.helpers.ui import (
    get_player_name,
    get_stone_color
)
from src.ui.board import draw_board
from window import (
    CELL_SIZE,
    FPS,
    PANEL_COLOR,
    PLAYGROUND_SIZE,
    TEXT_COLOR
)

DEBUG_PANEL_WIDTH = 440
MAX_DEPTH = 8
MAX_RADIUS = 3
LISTED_MOVES = 12

MOVE_LINE = re.compile(r"^\d+\s+(?:Black|White)\s+\((\d+), (\d+)\)")

CANDIDATE_COLOR = (60, 200, 90)
CHOSEN_COLOR = (255, 200, 0)
HOVER_COLOR = (255, 255, 255)
ILLEGAL_COLOR = (220, 50, 50)
CUT_COLOR = (150, 150, 155)
LAST_MOVE_COLOR = (230, 60, 60)
ERROR_COLOR = (255, 120, 120)
DIM_TEXT_COLOR = (170, 170, 175)
ROW_COLOR = (80, 80, 90)
BAR_COLOR = (90, 140, 210)
BOUND_PREFIX = {"exact": "", "upper": "<", "lower": ">"}


@dataclass
class DebugState:
    moves: list[tuple[int, int]]
    ply: int
    depth: int = 2
    radius: int = CANDIDATE_RADIUS
    exact_root: bool = False
    board: Board = field(default_factory=Board)
    forbidden: list[tuple[int, int]] = field(default_factory=list)
    result: str | int | None = None
    analyses: dict = field(default_factory=dict)
    message: str = ""
    # The cursor: a line of moves played from the displayed position, inside
    # the recorded tree. Empty path = the root of the analysis.
    path: list[tuple[int, int]] = field(default_factory=list)
    cursor_board: Board = field(default_factory=Board)
    cursor_forbidden: list[tuple[int, int]] = field(default_factory=list)
    cursor_result: str | int | None = None
    cursor_candidates: list[tuple[int, int]] = field(default_factory=list)
    cursor_illegal: set = field(default_factory=set)


def load_log_moves(
        path: str
) -> list[tuple[int, int]]:
    """Moves of a game log, in order. Stops at the first illegal move, so the
    result can always be replayed."""

    moves = []
    with open(path, encoding="utf-8") as log_file:
        for line in log_file:
            match = MOVE_LINE.match(line)
            if match:
                moves.append((int(match.group(1)), int(match.group(2))))

    board = Board()
    for number, (row, col) in enumerate(moves):
        try:
            board.play(Cell(row, col))
        except ValueError:
            return moves[:number]

    return moves


def replay(
        moves: list[tuple[int, int]],
        ply: int
) -> Board:

    board = Board()
    for row, col in moves[:ply]:
        board.play(Cell(row, col))

    return board


def set_path(
        state: DebugState,
        path: list[tuple[int, int]]
) -> None:
    """Move the cursor: rebuild the board, the candidate cells and the
    illegal ones for the node reached by `path`. Done once per move of the
    cursor, never at every frame (the double-three test is expensive)."""

    if not path:
        board = state.board
        state.path = []
        state.cursor_forbidden = state.forbidden
        state.cursor_result = state.result
    else:
        board = replay(state.moves, state.ply)
        for cell in path:
            board.play(Cell(*cell))
        state.path = list(path)
        state.cursor_result = compute_result(board)
        state.cursor_forbidden = (
            [] if state.cursor_result is not None else compute_forbidden(board)
        )
    state.cursor_board = board

    if state.cursor_result is not None:
        state.cursor_candidates = []
        state.cursor_illegal = set()
        return
    state.cursor_candidates = [
        (cell.row, cell.column)
        for cell in candidate_cells(board, state.radius)
    ]
    state.cursor_illegal = {
        cell for cell in state.cursor_candidates
        if not board.is_legal(Cell(*cell))
    }


def refresh(
        state: DebugState
) -> None:
    """Rebuild the board of the displayed position (cursor back at the
    root)."""

    state.board = replay(state.moves, state.ply)
    state.result = compute_result(state.board)
    state.forbidden = (
        [] if state.result is not None else compute_forbidden(state.board)
    )
    set_path(state, [])


def analysis_key(
        state: DebugState
) -> tuple:

    return (
        tuple(state.moves[:state.ply]),
        state.depth,
        state.radius,
        state.exact_root
    )


def current_analysis(
        state: DebugState
) -> Analysis | None:

    return state.analyses.get(analysis_key(state))


def run_analysis(
        state: DebugState,
        weights: HeuristicWeights
) -> None:

    if state.result is not None:
        state.message = "The game is over: nothing to analyse."
        return

    key = analysis_key(state)
    if key in state.analyses:
        return

    try:
        state.analyses[key] = analyse(
            state.board,
            weights,
            state.depth,
            state.radius,
            state.exact_root
        )
        state.message = ""
    except Exception as error:  # the tool must not crash on a search error
        state.message = f"Analysis failed: {type(error).__name__}: {error}"


def score_text(
        score: float
) -> str:
    """Full score, for the panel."""

    if abs(score) >= WIN_SCORE:
        return "WIN" if score > 0 else "LOSS"

    return f"{score:.0f}"


def short_score(
        score: float
) -> str:
    """Compact score, short enough to fit in a cell of the board."""

    if abs(score) >= WIN_SCORE:
        return "WIN" if score > 0 else "LOSS"
    if abs(score) >= 1000:
        return f"{score / 1000:.1f}k"

    return f"{score:.0f}"


def limit_text(
        value: float
) -> str:

    if value == float("inf"):
        return "+inf"
    if value == -float("inf"):
        return "-inf"

    return f"{value:.0f}"


def heat_color(
        t: float
) -> tuple[int, int, int]:
    """Red (t = 0, worst) to green (t = 1, best)."""

    return (int(200 - 140 * t), int(60 + 130 * t), int(60 + 20 * t))


def dim(
        color: tuple[int, int, int]
) -> tuple[int, int, int]:
    """Paler color, for scores that are only bounds."""

    return tuple(int(c * 0.55 + 70 * 0.45) for c in color)


def ranked_children(
        analysis: Analysis,
        index: int
) -> list[tuple[int, float]]:
    """Children of a node, best first for the side to move there, each with
    a color position t in [0, 1] that depends on the gap to the best score
    (logarithmic: equal scores share a color, a gap of 10 points is visible,
    a gap of 1000 is deep red)."""

    node = analysis.tree[index]
    sign = 1 if is_maximizing(node) else -1
    items = [(child, sign * analysis.tree[child].score)
             for child in node.children]
    if not items:
        return []
    items.sort(key=lambda item: -item[1])
    best = items[0][1]

    ranked = []
    for child, quality in items:
        gap = best - quality
        t = 1.0 if gap < 1 else max(0.0, 1 - math.log10(gap) / 3.5)
        ranked.append((child, t))

    return ranked


def draw_text(
        screen: pygame.Surface,
        font: pygame.font.Font,
        text: str,
        position: tuple[int, int],
        color: tuple[int, int, int] = TEXT_COLOR,
        center: bool = False
) -> None:

    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = position
    else:
        rect.topleft = position
    screen.blit(label, rect)


def draw_overlay(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        state: DebugState,
        analysis: Analysis | None,
        hovered: tuple[int, int] | None
) -> None:

    board = state.cursor_board

    if board.history and not state.path:
        row, col, _ = board.history[-1]
        pygame.draw.circle(
            screen, LAST_MOVE_COLOR, intersection_to_pixel(row, col), 5
        )
    # The moves of the cursor line, numbered like the moves of the game.
    for number, (row, col) in enumerate(state.path, start=state.ply + 1):
        text_color = (240, 240, 240) if board.grid[row][col] == BLACK \
            else (20, 20, 20)
        draw_text(screen, fonts["cell"], str(number),
                  intersection_to_pixel(row, col), text_color, center=True)

    if state.cursor_result is not None:
        return

    # Green border: every candidate cell of the displayed node.
    for row, col in state.cursor_candidates:
        rect = pygame.Rect(0, 0, CELL_SIZE - 8, CELL_SIZE - 8)
        rect.center = intersection_to_pixel(row, col)
        pygame.draw.rect(screen, CANDIDATE_COLOR, rect, 3)

    if analysis is None:
        return
    index = find_node(analysis, state.path)
    if index is None:
        return

    children = ranked_children(analysis, index)
    tried = {analysis.tree[child].cell for child, _ in children}

    # Candidates the search did not try: illegal (red cross) or cut off by
    # alpha-beta (grey dot).
    for cell in state.cursor_candidates:
        if cell in tried:
            continue
        x, y = intersection_to_pixel(*cell)
        if cell in state.cursor_illegal:
            pygame.draw.line(screen, ILLEGAL_COLOR, (x - 8, y - 8),
                             (x + 8, y + 8), 3)
            pygame.draw.line(screen, ILLEGAL_COLOR, (x - 8, y + 8),
                             (x + 8, y - 8), 3)
        else:
            pygame.draw.circle(screen, CUT_COLOR, (x, y), 6)

    # Score of every move the search tried, colored by the gap to the best.
    by_cell = {}
    for child, t in children:
        child_node = analysis.tree[child]
        by_cell[child_node.cell] = child
        exact = bound_kind(child_node) == "exact"
        color = heat_color(t) if exact else dim(heat_color(t))
        center = intersection_to_pixel(*child_node.cell)
        pygame.draw.circle(screen, color, center, STONE_RADIUS - 3)
        draw_text(screen, fonts["cell"], short_score(child_node.score),
                  center, (20, 20, 20), center=True)

    if children:
        best_cell = analysis.tree[children[0][0]].cell
        pygame.draw.circle(screen, CHOSEN_COLOR,
                           intersection_to_pixel(*best_cell),
                           STONE_RADIUS + 4, 4)

    if hovered in by_cell:
        pygame.draw.circle(screen, HOVER_COLOR,
                           intersection_to_pixel(*hovered),
                           STONE_RADIUS + 8, 2)
        # The line of play the search expects after the hovered move.
        player = board.current_player
        line = principal_line(analysis, by_cell[hovered])
        first = state.ply + len(state.path) + 1
        for number, (row, col) in enumerate(line, start=first):
            center = intersection_to_pixel(row, col)
            pygame.draw.circle(screen, get_stone_color(player), center,
                               STONE_RADIUS - 2)
            pygame.draw.circle(screen, HOVER_COLOR, center,
                               STONE_RADIUS - 2, 2)
            text_color = (240, 240, 240) if player == BLACK else (20, 20, 20)
            draw_text(screen, fonts["cell"], str(number), center,
                      text_color, center=True)
            player = WHITE if player == BLACK else BLACK


def path_text(
        path: list[tuple[int, int]]
) -> str:

    shown = path[-4:]
    text = "root"
    if len(path) > len(shown):
        text += " > ..."
    for row, col in shown:
        text += f" > ({row},{col})"

    return text


def draw_panel(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        state: DebugState,
        analysis: Analysis | None,
        hovered: tuple[int, int] | None
) -> None:

    screen.fill(PANEL_COLOR,
                (PLAYGROUND_SIZE, 0, DEBUG_PANEL_WIDTH, PLAYGROUND_SIZE))
    x = PLAYGROUND_SIZE + 16
    y = 12
    line = 21
    # Short lines: the panel is narrow (about 50 characters).
    keys = (
        "left / right: previous / next move",
        "shift + left / right: back / forward 2 moves",
        "home / end: first / last move",
        "A: analyse   E: exact root scores",
        "+ / -: depth   R: candidate radius",
        "click a scored cell: go down one level",
        "backspace / right click: go up",
        "enter: play this line   click: play a move",
        "hover a scored cell: expected line of play",
        "green border: candidate   red cross: illegal",
        "grey dot: cut   gold ring: best   pale: bound",
        "Q: quit",
    )
    keys_top = PLAYGROUND_SIZE - len(keys) * line - 8

    def write(text, color=TEXT_COLOR, font="small", gap=line):
        nonlocal y
        draw_text(screen, fonts[font], text, (x, y), color)
        y += gap

    board = state.board
    write("GOMOKU DEBUG", font="normal", gap=30)
    write(f"Move {state.ply} / {len(state.moves)}")
    if state.result is None:
        write(f"To play: {get_player_name(board.current_player)}")
    else:
        write(f"Game over: {state.result}", ERROR_COLOR)
    write(f"Captures: Black {board.captures[BLACK]}, "
          f"White {board.captures[WHITE]}")
    mode = "exact root scores" if state.exact_root else "real search"
    write(f"Depth {state.depth}   Radius {state.radius}   ({mode})",
          gap=line + 8)

    if analysis is None:
        write("Press A to analyse this position.", DIM_TEXT_COLOR)
    else:
        rate = analysis.evaluations / max(analysis.seconds, 1e-9)
        write(f"Time {analysis.seconds:.2f} s   Leaves "
              f"{analysis.evaluations} ({rate:.0f}/s)")
        write(f"Root candidates {len(analysis.candidates)}, "
              f"legal moves tried {len(analysis.moves)}")
        write("Nodes per level:", DIM_TEXT_COLOR, gap=line - 3)
        write("  " + "  ".join(
            f"L{level}: {count}"
            for level, count in sorted(analysis.nodes_per_level.items())
        ), DIM_TEXT_COLOR)
        if analysis.truncated:
            write("Tree truncated (too large): deeper nodes not recorded.",
                  ERROR_COLOR)
        y += 8
        draw_node_block(screen, fonts, state, analysis, hovered, x, y,
                        keys_top, line)

    if state.message:
        draw_text(screen, fonts["small"], state.message,
                  (x, keys_top - line - 4), ERROR_COLOR)

    y = keys_top
    for text in keys:
        write(text, DIM_TEXT_COLOR)


def draw_node_block(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        state: DebugState,
        analysis: Analysis,
        hovered: tuple[int, int] | None,
        x: int,
        y: int,
        keys_top: int,
        line: int
) -> None:
    """The displayed node: its path, its score and window, and its moves
    ranked."""

    index = find_node(analysis, state.path)
    if index is None:
        draw_text(screen, fonts["small"], "This line was never searched.",
                  (x, y), ERROR_COLOR)
        return
    node = analysis.tree[index]
    board = state.cursor_board

    def write(text, color=TEXT_COLOR, font="small", gap=line):
        nonlocal y
        draw_text(screen, fonts[font], text, (x, y), color)
        y += gap

    write("Path: " + path_text(state.path), font="normal", gap=26)
    if state.cursor_result is not None:
        write(f"Game over at this node: {state.cursor_result}", ERROR_COLOR)
        return
    role = "AI maximizes" if is_maximizing(node) else "opponent minimizes"
    write(f"{get_player_name(board.current_player)} to play ({role})")
    if index != 0:
        kind = bound_kind(node)
        write(f"Node score {BOUND_PREFIX[kind]}{score_text(node.score)} "
              f"({kind}), window [{limit_text(node.alpha)}, "
              f"{limit_text(node.beta)}]")
        write(f"Subtree: {node.nodes} nodes, {node.leaves} leaves, "
              f"{node.seconds:.2f} s")
    legal = len(state.cursor_candidates) - len(state.cursor_illegal)
    cut = legal - len(node.children)
    write(f"Moves explored {len(node.children)} of {legal} legal candidates"
          + (f" ({cut} cut)" if cut > 0 else ""))
    y += 6

    ranked = ranked_children(analysis, index)
    if not ranked:
        write("No move below this node (leaf or terminal position).",
              DIM_TEXT_COLOR)
        return
    write("Moves, best first for the side to play", font="normal", gap=26)
    write("'<' value <= shown, '>' value >= shown. Bar = nodes.",
          DIM_TEXT_COLOR, gap=line + 4)
    max_rows = max(3, min(LISTED_MOVES, (keys_top - y - 60) // line))
    most_nodes = max((analysis.tree[child].nodes for child, _ in ranked),
                     default=1)
    for rank, (child, _) in enumerate(ranked[:max_rows], start=1):
        child_node = analysis.tree[child]
        if child_node.cell == hovered:
            pygame.draw.rect(screen, ROW_COLOR,
                             (x - 6, y - 2, DEBUG_PANEL_WIDTH - 20, line))
        text = (BOUND_PREFIX[bound_kind(child_node)]
                + score_text(child_node.score))
        mark = "*" if rank == 1 else " "
        write(f"{mark}{rank:2d}. ({child_node.cell[0]:2d},"
              f"{child_node.cell[1]:2d}) {text:>8}", gap=0)
        width = int(110 * child_node.nodes / most_nodes)
        pygame.draw.rect(screen, BAR_COLOR,
                         (x + 215, y + 3, max(width, 1), 12))
        draw_text(screen, fonts["small"], str(child_node.nodes),
                  (x + 215 + 115, y), DIM_TEXT_COLOR)
        y += line
    if len(ranked) > max_rows:
        write(f"... and {len(ranked) - max_rows} more", DIM_TEXT_COLOR)
    for child, _ in ranked:
        child_node = analysis.tree[child]
        if child_node.cell == hovered:
            y += 4
            write(f"({hovered[0]},{hovered[1]}): "
                  f"{BOUND_PREFIX[bound_kind(child_node)]}"
                  f"{score_text(child_node.score)}, {child_node.nodes} nodes, "
                  f"{child_node.leaves} leaves, {child_node.seconds:.2f} s")
            break


def render(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        state: DebugState,
        hovered: tuple[int, int] | None
) -> None:

    analysis = current_analysis(state)
    draw_board(screen, state.cursor_board, state.cursor_forbidden)
    draw_overlay(screen, fonts, state, analysis, hovered)
    draw_panel(screen, fonts, state, analysis, hovered)
    pygame.display.flip()


def go_to(
        state: DebugState,
        ply: int
) -> None:

    state.ply = max(0, min(len(state.moves), ply))
    state.message = ""
    refresh(state)


def go_up(
        state: DebugState
) -> None:

    if state.path:
        set_path(state, state.path[:-1])


def commit_line(
        state: DebugState
) -> None:
    """Play the line of the cursor on the displayed position (the following
    moves of the loaded game are dropped)."""

    if not state.path:
        return
    count = len(state.path)
    state.moves = state.moves[:state.ply] + [tuple(c) for c in state.path]
    go_to(state, state.ply + count)


def handle_key(
        state: DebugState,
        key: int
) -> str | None:
    """Apply a key. Returns "quit", "analyse" or None."""

    if key in (pygame.K_q, pygame.K_ESCAPE):
        return "quit"
    # Shift moves by two plies: one full turn (one move of each player).
    step = 2 if pygame.key.get_mods() & pygame.KMOD_SHIFT else 1
    if key == pygame.K_BACKSPACE:
        if state.path:
            go_up(state)
        else:
            go_to(state, state.ply - 1)
    elif key == pygame.K_LEFT:
        go_to(state, state.ply - step)
    elif key == pygame.K_RIGHT:
        go_to(state, state.ply + step)
    elif key == pygame.K_HOME:
        go_to(state, 0)
    elif key == pygame.K_END:
        go_to(state, len(state.moves))
    elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        commit_line(state)
    elif key == pygame.K_e:
        state.exact_root = not state.exact_root
        set_path(state, [])
    elif key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
        state.depth = min(MAX_DEPTH, state.depth + 1)
        set_path(state, [])
    elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
        state.depth = max(1, state.depth - 1)
        set_path(state, [])
    elif key == pygame.K_r:
        state.radius = state.radius % MAX_RADIUS + 1
        set_path(state, [])
    elif key == pygame.K_a:
        return "analyse"

    return None


def handle_click(
        state: DebugState,
        pos: tuple[int, int]
) -> None:
    """On a scored cell: go down one level. Elsewhere, at the root: play a
    move on the displayed position."""

    intersection = pixel_to_intersection(*pos)
    if intersection is None:
        return

    analysis = current_analysis(state)
    if analysis is not None and state.cursor_result is None:
        index = find_node(analysis, state.path)
        if index is not None:
            for child in analysis.tree[index].children:
                if analysis.tree[child].cell == intersection:
                    set_path(state, state.path + [intersection])
                    return

    if state.path:
        state.message = "Go back to the root (backspace) to play a move."
        return
    if state.result is not None:
        return
    if state.board.is_legal(Cell(*intersection)):
        state.moves = state.moves[:state.ply] + [intersection]
        go_to(state, state.ply + 1)


def main() -> None:

    moves = []
    if len(sys.argv) > 2:
        print("usage: python3 -m src.debug.gomoku_debug [game_log]")
        sys.exit(2)
    if len(sys.argv) == 2:
        moves = load_log_moves(sys.argv[1])

    pygame.init()
    try:
        screen = pygame.display.set_mode(
            (PLAYGROUND_SIZE + DEBUG_PANEL_WIDTH, PLAYGROUND_SIZE)
        )
        pygame.display.set_caption("GOMOKU DEBUG")
        fonts = {
            "normal": pygame.font.Font(None, 28),
            "small": pygame.font.Font(None, 21),
            "cell": pygame.font.Font(None, 19),
        }
        clock = pygame.time.Clock()
        weights = generate_weights()

        state = DebugState(moves=moves, ply=len(moves))
        refresh(state)

        running = True
        while running:
            request = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    action = handle_key(state, event.key)
                    if action == "quit":
                        running = False
                    elif action == "analyse":
                        request = action
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        handle_click(state, event.pos)
                    elif event.button == 3:
                        go_up(state)
            if not running:
                break

            hovered = pixel_to_intersection(*pygame.mouse.get_pos())
            render(screen, fonts, state, hovered)

            if request == "analyse":
                # The window freezes during the search: say it first.
                state.message = "Analysing..."
                render(screen, fonts, state, hovered)
                state.message = ""
                run_analysis(state, weights)

            clock.tick(FPS)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
