import pytest
from board import (
    BLACK,
    WHITE
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
from tests.utils import (
    create_empty_grid,
    create_line,
    place_stones
)


@pytest.mark.parametrize(
    "start, direction",
    [
        ((9, 8), (0, 1)),
        ((8, 9), (1, 0)),
        ((8, 8), (1, 1)),
        ((8, 10), (1, -1))
    ]
)
def test_three_open_stones(start, direction):
    grid = create_empty_grid()

    cells = create_line(start, direction, 3)
    place_stones(grid, cells, BLACK)

    score = evaluate_alignments(grid, BLACK)

    assert score == THREE_OPEN_STONES


@pytest.mark.parametrize(
    "opponent_cell",
    [
        (9, 7),
        (9, 11)
    ]
)
def test_three_blocked_stones(opponent_cell):
    grid = create_empty_grid()

    place_stones(grid, [(9, 8), (9, 9), (9, 10)], BLACK)
    grid[opponent_cell[0]][opponent_cell[1]] = WHITE

    score = evaluate_alignments(grid, BLACK)

    assert score == THREE_BLOCKED_STONES


@pytest.mark.parametrize(
    "start, direction",
    [
        ((9, 8), (0, 1)),
        ((8, 9), (1, 0)),
        ((8, 8), (1, 1)),
        ((8, 10), (1, -1))
    ]
)
def test_four_open_stones(start, direction):
    grid = create_empty_grid()

    cells = create_line(start, direction, 4)
    place_stones(grid, cells, BLACK)

    score = evaluate_alignments(grid, BLACK)

    assert score == FOUR_OPEN_STONES
