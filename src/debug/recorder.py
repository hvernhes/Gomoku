"""Search recorder for the visual debug tool.

Runs one analysis of a position and keeps the search tree: every node with
its move, its score, its alpha-beta window, its subtree size and its
children. The search code is not modified: the functions of the minimax
module are wrapped for the duration of the analysis (like the counters of the
tests) and always restored.

The tree is capped (MAX_RECORDED_NODES) so a deep search cannot exhaust the
memory; the counters stay exact even when the tree is truncated.
"""
import time
from dataclasses import dataclass, field

import src.ai.minimax as minimax_module
from src.ai.candidates import CANDIDATE_RADIUS
from src.ai.candidates import candidate_cells as original_candidate_cells
from src.ai.weights import HeuristicWeights
from src.game.Board import Board

INFINITY = float("inf")
MAX_RECORDED_NODES = 300_000


@dataclass
class Node:
    cell: tuple[int, int] | None    # move that led to this node (None: root)
    level: int                      # 0 = the analysed position
    alpha: float                    # window the node was called with
    beta: float
    score: float | None = None      # value returned by minimax
    nodes: int = 1                  # size of the subtree (itself included)
    leaves: int = 0                 # evaluations done in the subtree
    own_leaves: int = 0
    seconds: float = 0.0
    children: list[int] = field(default_factory=list)   # indices in the tree


@dataclass
class RootMove:
    cell: tuple[int, int]
    score: float      # value returned by minimax for this root move
    exact: bool       # False: only a bound (the real value is <= score)
    nodes: int        # nodes explored in its subtree (itself included)
    leaves: int       # evaluations done in its subtree
    seconds: float


@dataclass
class Analysis:
    depth: int
    radius: int
    exact_root: bool
    candidates: list[tuple[int, int]]   # root candidates, before legality
    moves: list[RootMove]               # legal root moves, in the tried order
    best: tuple[int, int] | None
    nodes_per_level: dict[int, int]     # level 0 = the root position
    evaluations: int
    seconds: float
    tree: list[Node]                    # tree[0] is the root
    truncated: bool                     # True if the tree hit the size cap


def bound_kind(
        node: Node
) -> str:
    """"exact", "upper" (the real value is <= score: every child failed low)
    or "lower" (the real value is >= score: a beta cut happened)."""

    if node.score is None:
        return "exact"
    if node.score <= node.alpha:
        return "upper"
    if node.score >= node.beta:
        return "lower"

    return "exact"


def is_maximizing(
        node: Node
) -> bool:
    """The side to move at the root is the AI: it maximizes at even levels."""

    return node.level % 2 == 0


def find_node(
        analysis: Analysis,
        path: list[tuple[int, int]]
) -> int | None:
    """Index of the node reached from the root by the moves of `path`, or
    None if the search never played this line."""

    index = 0
    for cell in path:
        for child in analysis.tree[index].children:
            if analysis.tree[child].cell == tuple(cell):
                index = child
                break
        else:
            return None

    return index


def best_child(
        analysis: Analysis,
        index: int
) -> int | None:
    """The child the side to move prefers (first one on a tie)."""

    node = analysis.tree[index]
    if not node.children:
        return None
    pick = max if is_maximizing(node) else min

    return pick(node.children, key=lambda child: analysis.tree[child].score)


def principal_line(
        analysis: Analysis,
        index: int
) -> list[tuple[int, int]]:
    """The line of play from a node: its own move, then at each node the
    preferred child, down to the leaves of the recorded tree."""

    line = []
    while True:
        node = analysis.tree[index]
        if node.cell is not None:
            line.append(node.cell)
        child = best_child(analysis, index)
        if child is None:
            return line
        index = child


def _best_move_exact(
        board: Board,
        weights: HeuristicWeights,
        depth: int,
        counted_minimax
) -> tuple[int, int] | None:
    """Same loop as best_move, but every root move is searched with the full
    window (no alpha cut at the root): every score is exact."""

    if depth < 1:
        raise ValueError("depth must be at least 1")

    ai_player = board.current_player
    best = None
    best_score = -INFINITY
    for cell in list(minimax_module._moves_to_try(board)):
        board.play(cell)
        try:
            score = counted_minimax(board, weights, depth - 1, ai_player)
        finally:
            board.undo()
        if score > best_score:
            best_score = score
            best = (cell.row, cell.column)

    return best


def analyse(
        board: Board,
        weights: HeuristicWeights,
        depth: int,
        radius: int = CANDIDATE_RADIUS,
        exact_root: bool = False
) -> Analysis:
    """Analyse the position for the current player. The board is left
    exactly as it was. exact_root=False runs the real best_move (the scores
    of the root moves that are not the best are then only bounds)."""

    root_length = len(board.history)
    levels = {0: 1}
    root_candidates = []
    stats = {"evaluations": 0, "truncated": False}
    tree = [Node(None, 0, -INFINITY, INFINITY)]
    stack = [0]     # indices of the nodes being searched, the root first

    original_minimax = minimax_module.minimax
    original_evaluate = minimax_module.evaluate
    original_candidates = minimax_module.candidate_cells

    def counted_candidates(b):
        cells = original_candidate_cells(b, radius)
        if len(b.history) == root_length and not root_candidates:
            root_candidates.extend((c.row, c.column) for c in cells)
        return cells

    def counted_evaluate(b, w, player):
        stats["evaluations"] += 1
        tree[stack[-1]].own_leaves += 1
        return original_evaluate(b, w, player)

    def counted_minimax(b, w, remaining, ai_player,
                        alpha=-INFINITY, beta=INFINITY):
        level = len(b.history) - root_length
        levels[level] = levels.get(level, 0) + 1
        if len(tree) >= MAX_RECORDED_NODES:
            stats["truncated"] = True
            return original_minimax(b, w, remaining, ai_player, alpha, beta)

        row, col, _ = b.history[-1]
        index = len(tree)
        node = Node((row, col), level, alpha, beta)
        tree.append(node)
        tree[stack[-1]].children.append(index)
        stack.append(index)
        started = time.perf_counter()
        try:
            score = original_minimax(b, w, remaining, ai_player, alpha, beta)
        finally:
            stack.pop()
        node.score = score
        node.seconds = time.perf_counter() - started
        node.nodes = 1 + sum(tree[child].nodes for child in node.children)
        node.leaves = node.own_leaves + sum(
            tree[child].leaves for child in node.children)

        return score

    minimax_module.minimax = counted_minimax
    minimax_module.evaluate = counted_evaluate
    minimax_module.candidate_cells = counted_candidates
    try:
        start = time.perf_counter()
        if exact_root:
            best = _best_move_exact(board, weights, depth, counted_minimax)
        else:
            cell = minimax_module.best_move(board, weights, depth)
            best = None if cell is None else (cell.row, cell.column)
        seconds = time.perf_counter() - start
    finally:
        minimax_module.minimax = original_minimax
        minimax_module.evaluate = original_evaluate
        minimax_module.candidate_cells = original_candidates

    moves = []
    for child in tree[0].children:
        node = tree[child]
        moves.append(RootMove(
            node.cell,
            node.score,
            bound_kind(node) == "exact",
            node.nodes,
            node.leaves,
            node.seconds
        ))

    return Analysis(
        depth,
        radius,
        exact_root,
        root_candidates,
        moves,
        best,
        levels,
        stats["evaluations"],
        seconds,
        tree,
        stats["truncated"]
    )
