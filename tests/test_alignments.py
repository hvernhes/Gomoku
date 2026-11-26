import pytest
from board import BLACK
from heuristic import (
    FIVE_OPEN_STONES,
    FOUR_BLOCKED_STONES,
    FOUR_HALF_BLOCKED_STONES,
    FOUR_OPEN_STONES,
    THREE_BLOCKED_STONES,
    THREE_HALF_BLOCKED_STONES,
    THREE_OPEN_STONES
)
from src.ai.heuristic import evaluate_alignments
from src.ai.weights import generate_weights
from src.helpers.utils import opponent_of
from tests.utils import (
    create_empty_grid,
    create_line,
    get_player_situation,
    place_stones
)


def test_empty_grid(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == 0


def test_two_stones(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, [(9, 9), (9, 10)], player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == 0


def test_two_stones_separated_by_opponent(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, [(9, 8), (9, 10)], player)
    place_stones(grid, [(9, 9)], opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == 0


def test_three_stones_with_two_holes(   
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, [(9, 8), (9, 10), (9, 12)], player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == 0


def test_four_stones_with_two_holes(   
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, [(9, 8), (9, 10), (9, 11), (9, 13)], player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == 2 * THREE_OPEN_STONES


@pytest.mark.parametrize(
    "start, direction",
    [
        ((9, 8), (0, 1)),
        ((8, 9), (1, 0)),
        ((8, 8), (1, 1)),
        ((8, 10), (1, -1))
    ]
)
def test_three_open_stones(
    start: tuple[int, int],
    direction: tuple[int, int]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line(start, direction, 3)
    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == THREE_OPEN_STONES


@pytest.mark.parametrize(
    "start, direction",
    [
        ((0, 0), (0, 1)),
        ((0, 0), (1, 0)),
        ((0, 0), (1, 1)),
        ((18, 18), (-1, 0)),
        ((18, 18), (0, -1)),
        ((18, 18), (-1, -1))
    ]
)
def test_three_stones_on_board_edge(
    start: tuple[int, int],
    direction: tuple[int, int]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line(start, direction, 3)
    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == THREE_HALF_BLOCKED_STONES


@pytest.mark.parametrize(
    "opponent",
    [
        [(9, 7)],
        [(9, 11)]
    ]
)
def test_three_half_blocked_stones(
    opponent: list[tuple[int, int]]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line((9, 8), (0, 1), 3)
    place_stones(grid, cells, player)
    place_stones(grid, opponent, opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == THREE_HALF_BLOCKED_STONES


def test_three_blocked_stones(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line((9, 8), (0, 1), 3)
    place_stones(grid, cells, player)
    place_stones(grid, [(9, 7), (9, 11)], opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == THREE_BLOCKED_STONES


@pytest.mark.parametrize(
    "cells",
    [
        [(9, 8), (9, 10), (9, 11)],
        [(9, 8), (9, 9), (9, 11)]
    ]
)
def test_three_stones_with_hole(
    cells: list[tuple[int, int]]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == THREE_OPEN_STONES


@pytest.mark.parametrize(
    "cells",
    [
        [(9, 8), (9, 10), (9, 11)],
        [(9, 8), (9, 9), (9, 11)]
    ]
)
@pytest.mark.parametrize(
    "opponent",
    [
        [(9, 7)],
        [(9, 12)]
    ]
)
def test_three_half_blocked_stones_with_hole(
        cells: list[tuple[int, int]],
        opponent: list[tuple[int, int]]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, cells, player)
    place_stones(grid, opponent, opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == THREE_HALF_BLOCKED_STONES


@pytest.mark.parametrize(
    "cells",
    [
        [(9, 8), (9, 10), (9, 11)],
        [(9, 8), (9, 9), (9, 11)]
    ]
)
def test_three_blocked_stones_with_hole(
        cells: list[tuple[int, int]]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, cells, player)
    place_stones(grid, [(9, 7), (9, 12)], opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == THREE_BLOCKED_STONES


@pytest.mark.parametrize(
    "cells",
    [
        [(0, 0), (0, 2), (0, 3)],
        [(0, 0), (0, 1), (0, 3)],
        [(0, 0), (2, 2), (3, 3)],
        [(0, 0), (1, 1), (3, 3)],
        [(0, 0), (2, 0), (3, 0)],
        [(0, 0), (1, 0), (3, 0)],
        [(18, 18), (18, 16), (18, 15)],
        [(18, 18), (18, 17), (18, 15)],
        [(18, 18), (16, 16), (15, 15)],
        [(18, 18), (17, 17), (15, 15)],
        [(18, 18), (16, 18), (15, 18)],
        [(18, 18), (17, 18), (15, 18)]
    ]
)
def test_three_stones_with_hole_on_board_edge(
    cells: list[tuple[int, int]],
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == THREE_HALF_BLOCKED_STONES


@pytest.mark.parametrize(
    "start, direction",
    [
        ((9, 8), (0, 1)),
        ((8, 9), (1, 0)),
        ((8, 8), (1, 1)),
        ((8, 10), (1, -1))
    ]
)
def test_four_open_stones(
    start: tuple[int, int],
    direction: tuple[int, int]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line(start, direction, 4)
    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FOUR_OPEN_STONES


@pytest.mark.parametrize(
    "start, direction",
    [
        ((0, 0), (0, 1)),
        ((0, 0), (1, 0)),
        ((0, 0), (1, 1)),
        ((18, 18), (-1, 0)),
        ((18, 18), (0, -1)),
        ((18, 18), (-1, -1))
    ]
)
def test_four_stones_on_board_edge(
    start: tuple[int, int],
    direction: tuple[int, int]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line(start, direction, 4)
    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FOUR_HALF_BLOCKED_STONES


@pytest.mark.parametrize(
    "opponent",
    [
        [(7, 9)],
        [(12, 9)]
    ]
)
def test_four_half_blocked_stones(
    opponent: tuple[int, int]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line((8, 9), (1, 0), 4)
    place_stones(grid, cells, player)
    place_stones(grid, opponent, opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FOUR_HALF_BLOCKED_STONES


def test_four_blocked_stones(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line((8, 9), (1, 0), 4)
    place_stones(grid, cells, player)
    place_stones(grid, [(7, 9), (12, 9)], opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FOUR_BLOCKED_STONES


@pytest.mark.parametrize(
    "cells",
    [
        [(9, 8), (9, 10), (9, 11), (9, 12)],
        [(9, 8), (9, 9), (9, 11), (9, 12)],
        [(9, 8), (9, 9), (9, 10), (9, 12)],
    ]
)
def test_four_stones_with_hole(
    cells: list[tuple[int, int]]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FOUR_HALF_BLOCKED_STONES


@pytest.mark.parametrize(
    "cells",
    [
        [(8, 8), (10, 10), (11, 11), (12, 12)],
        [(8, 8), (9, 9), (11, 11), (12, 12)],
        [(8, 8), (9, 9), (10, 10), (12, 12)]
    ]
)
@pytest.mark.parametrize(
    "opponent",
    [
        [(7, 7)],
        [(13, 13)],
        [(7, 7), (13, 13)]
    ]
)
def test_four_blocked_stones_with_hole(
        cells: list[tuple[int, int]],
        opponent: list[tuple[int, int]]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, cells, player)
    place_stones(grid, opponent, opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FOUR_HALF_BLOCKED_STONES


@pytest.mark.parametrize(
    "cells",
    [
        [(0, 0), (0, 2), (0, 3), (0, 4)],
        [(0, 0), (0, 1), (0, 3), (0, 4)],
        [(0, 0), (0, 1), (0, 2), (0, 4)],
        [(0, 0), (2, 2), (3, 3), (4, 4)],
        [(0, 0), (1, 1), (3, 3), (4, 4)],
        [(0, 0), (1, 1), (2, 2), (4, 4)],
        [(0, 0), (2, 0), (3, 0), (4, 0)],
        [(0, 0), (1, 0), (3, 0), (4, 0)],
        [(0, 0), (1, 0), (2, 0), (4, 0)],
        [(18, 18), (18, 16), (18, 15), (18, 14)],
        [(18, 18), (18, 17), (18, 15), (18, 14)],
        [(18, 18), (18, 17), (18, 16), (18, 14)],
        [(18, 18), (16, 16), (15, 15), (14, 14)],
        [(18, 18), (17, 17), (15, 15), (14, 14)],
        [(18, 18), (17, 17), (16, 16), (14, 14)],
        [(18, 18), (16, 18), (15, 18), (14, 18)],
        [(18, 18), (17, 18), (15, 18), (14, 18)],
        [(18, 18), (17, 18), (16, 18), (14, 18)],
    ]
)
def test_four_stones_with_hole_on_board_edge(
    cells: list[tuple[int, int]],
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FOUR_HALF_BLOCKED_STONES


@pytest.mark.parametrize(
    "start, direction",
    [
        ((9, 8), (0, -1)),
        ((8, 9), (-1, 0)),
        ((8, 8), (-1, -1)),
        ((8, 10), (-1, 1))
    ]
)
def test_five_stones(
    start: tuple[int, int],
    direction: tuple[int, int]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line(start, direction, 5)
    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FIVE_OPEN_STONES


@pytest.mark.parametrize(
    "opponent_cell",
    [
        [(4, 4)],
        [(10, 10)],
        [(4, 4), (10, 10)]
    ]
)
def test_five_stones_with_blocked_end(
    opponent_cell: list[tuple[int, int]]
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line((5, 5), (1, 1), 5)
    place_stones(grid, cells, player)
    place_stones(grid, opponent_cell, opponent_of(player))

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FIVE_OPEN_STONES


def test_five_stones_with_hole(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    place_stones(
        grid,
        [(9, 8), (9, 9), (9, 11), (9, 12), (9, 13)],
        player
    )

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FOUR_HALF_BLOCKED_STONES


def test_six_stones(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    cells = create_line((9, 7), (0, 1), 6)
    place_stones(grid, cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == FIVE_OPEN_STONES


def test_two_crossing_alignments(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    horizontal_cells = create_line((9, 7), (0, 1), 4)
    vertical_cells = create_line((7, 9), (1, 0), 4)

    place_stones(grid, horizontal_cells, player)
    place_stones(grid, vertical_cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == 2 * FOUR_OPEN_STONES


def test_two_alignments_starting_with_the_same_stone(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    horizontal_cells = create_line((9, 9), (0, 1), 4)
    vertical_cells = create_line((9, 9), (1, -1), 4)

    place_stones(grid, horizontal_cells, player)
    place_stones(grid, vertical_cells, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == 2 * FOUR_OPEN_STONES


def test_two_parallel_alignments(
) -> None:

    grid = create_empty_grid()
    weights = generate_weights()
    player = BLACK

    first = create_line((8, 7), (0, 1), 4)
    second = create_line((10, 7), (0, 1), 4)

    place_stones(grid, first, player)
    place_stones(grid, second, player)

    player_situation = get_player_situation(grid, player)
    score = evaluate_alignments(player_situation.aligned, weights)

    assert score == 2 * FOUR_OPEN_STONES
