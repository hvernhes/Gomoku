from board import (
    NUMBER_OF_CELLS,
    EMPTY,
    BLACK
)
from heuristic import (
    CENTRAL,
    CENTRAL_MEDIUM,
    CENTRAL_FAR,
    FIVE_OPEN_STONES,
    FOUR_BLOCKED_STONES,
    FOUR_OPEN_STONES,
    STONE_CAPTURE,
    THREE_BLOCKED_STONES,
    THREE_OPEN_STONES
)

from src.ai.heuristic import evaluate_alignments


GRID = [
    [EMPTY] * NUMBER_OF_CELLS
    for _ in range(NUMBER_OF_CELLS)
]


def test_alignments_of_free(
) -> None:

    grid = GRID.copy()
    contiguous_cells = [
        (9, 9),
        (10, 10),
        (11, 11)
    ]

    for cell in contiguous_cells:
        grid[cell[0]][cell[1]] = BLACK

    score = evaluate_alignments(grid, BLACK)

    assert score == THREE_OPEN_STONES
