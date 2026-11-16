import pygame
import sys
from board import (
    BLACK,
    BLACK_STONE_COLOR,
    EMPTY,
    LINE_COLOR,
    NUMBER_OF_CELLS,
    STONE_RADIUS,
    WHITE,
    WHITE_STONE_COLOR
)
from src.ai.heuristic import evaluation
from src.game.Board import Board
from src.game.Cell import Cell
from src.helpers.computation import pixel_to_intersection
from src.ui.window import draw_all_window
from window import (
    BIG_FONT,
    FORBIDDEN_COLOR,
    FPS,
    GHOST_ALPHA,
    NORMAL_FONT,
    OVERLAY_COLOR,
    PANEL_WIDTH,
    PLAYGROUND_SIZE,
    SMALL_FONT,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH
)


UNDO_BUTTON = pygame.Rect(PLAYGROUND_SIZE + 30, 40, PANEL_WIDTH - 60, 44)
POPUP_RECT = pygame.Rect(0, 0, 380, 190)
POPUP_RECT.center = (PLAYGROUND_SIZE // 2, PLAYGROUND_SIZE // 2)
POPUP_UNDO = pygame.Rect(POPUP_RECT.left + 30, POPUP_RECT.bottom - 70, 150, 44)
POPUP_RESTART = pygame.Rect(POPUP_UNDO.right + 20, POPUP_UNDO.top, 150, 44)


def compute_forbidden(board):
    """Intersections libres interdites au joueur courant (double-three).
    Calcule une fois par coup, pas a chaque image : c'est couteux."""

    return [(row, col)
            for row in range(NUMBER_OF_CELLS)
            for col in range(NUMBER_OF_CELLS)
            if board.get_cell_state(Cell(row, col)) == EMPTY and not board.is_legal(Cell(row, col))]


def compute_result(board):
    """BLACK, WHITE, DRAW (plateau plein) ou None si la partie continue."""
    winner = board.winner()
    if winner is not None:
        return winner
    if board.is_full():
        return "draw"
    return None


def make_ghost(color):
    """Pierre semi-transparente de la couleur donnee (creee une fois)."""

    size = 2 * STONE_RADIUS
    ghost = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (STONE_RADIUS, STONE_RADIUS)
    pygame.draw.circle(ghost, (*color, GHOST_ALPHA), center, STONE_RADIUS)
    pygame.draw.circle(ghost, (*LINE_COLOR, GHOST_ALPHA), center,
                       STONE_RADIUS, 1)

    return ghost


def make_overlay():
    overlay = pygame.Surface((PLAYGROUND_SIZE, PLAYGROUND_SIZE), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    return overlay


def open_window(
        window_width,
        window_height,
        window_title
) -> pygame.Surface:

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(window_title)

    return screen


def handle_click(pos, board, result):
    changed = False

    undo_clicked = (
        UNDO_BUTTON.collidepoint(pos)
        or (
            result is not None
            and POPUP_UNDO.collidepoint(pos)
        )
    )

    if undo_clicked:
        if board.history:
            board.undo()
            changed = True

    elif result is not None and POPUP_RESTART.collidepoint(pos):
        board = Board()
        changed = True

    elif result is None:
        cell = pixel_to_intersection(*pos)

        if cell is not None:
            cell = Cell(*cell)

            if board.is_legal(cell):
                player = board.current_player
                board.play(cell)

                value = evaluation(board.grid, player)
                print(value)

                changed = True

    return board, changed


def main():

    pygame.init()

    try:
        screen = open_window(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            WINDOW_TITLE
        )

        fonts = {
            "big": pygame.font.Font(None, BIG_FONT),
            "normal": pygame.font.Font(None, NORMAL_FONT),
            "small": pygame.font.Font(None, SMALL_FONT),
        }
        ghosts = {
            BLACK: make_ghost(BLACK_STONE_COLOR),
            WHITE: make_ghost(WHITE_STONE_COLOR),
            "RED": make_ghost(FORBIDDEN_COLOR)
        }
        overlay = make_overlay()
        clock = pygame.time.Clock()
        board = Board()
        result = None
        forbidden = compute_forbidden(board)

        running = True
        while running:

            changed = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    board, changed = handle_click(
                        event.pos,
                        board,
                        result
                    )

                    if changed:
                        break

            if changed:
                result = compute_result(board)
                forbidden = (
                    []
                    if result is not None
                    else compute_forbidden(board)
                )

            if not running:
                break

            draw_all_window(
                screen,
                board,
                fonts,
                result,
                forbidden,
                ghosts,
                overlay
            )

            pygame.display.flip()
            clock.tick(FPS)

    finally:

        pygame.quit()


if __name__ == "__main__":

    sys.exit(main())
