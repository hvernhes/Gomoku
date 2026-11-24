import pytest
from board import (
    BLACK,
    WHITE
)
from heuristic import STONE_CAPTURE
from src.ai.captures_evaluation import evaluate_captures
from tests.utils import (
    create_capture_configuration,
    create_empty_grid,
    place_stones
)


@pytest.mark.parametrize(
    "direction",
    [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1)
    ]
)
def test_one_possible_capture_in_each_direction(
    direction
) -> None:

    grid = create_empty_grid()

    create_capture_configuration(
        grid,
        (9, 9),
        direction,
        WHITE
    )

    score = evaluate_captures(grid, 0, WHITE)

    assert score == STONE_CAPTURE


def test_multiple_possible_captures_from_one_stone(
) -> None:

    grid = create_empty_grid()

    directions = [
        (0, -1),
        (1, 0),
        (-1, -1)
    ]

    for direction in directions:
        create_capture_configuration(
            grid,
            (9, 9),
            direction,
            WHITE
        )

    score = evaluate_captures(grid, 0, WHITE)

    assert score == 3 * STONE_CAPTURE


def test_possible_captures_from_different_player_stones(
) -> None:

    grid = create_empty_grid()

    create_capture_configuration(
        grid,
        (5, 5),
        (0, 1),
        WHITE
    )
    create_capture_configuration(
        grid,
        (12, 12),
        (-1, 1),
        WHITE
    )

    score = evaluate_captures(grid, 0, WHITE)

    assert score == 2 * STONE_CAPTURE


@pytest.mark.parametrize(
    "opponent_cells, extra_cells",
    [
        # Une seule pierre adverse
        ([(9, 10)], []),

        # Deux pierres adverses, mais pas de case vide après
        ([(9, 10), (9, 11)], [(9, 12)]),

        # Une case vide entre les deux pierres adverses
        ([(9, 10), (9, 12)], []),

        # Une pierre adverse puis une pierre du joueur
        ([(9, 10)], [(9, 11)])
    ]
)
def test_no_capture_with_invalid_pattern(
    opponent_cells: list[tuple[int, int]],
    extra_cells: list[tuple[int, int]]
):

    grid = create_empty_grid()

    place_stones(grid, [(9, 9)], WHITE)
    place_stones(grid, opponent_cells, BLACK)
    place_stones(grid, extra_cells, WHITE)

    score = evaluate_captures(grid, 0, WHITE)

    assert score == 0


def test_no_capture_out_of_bounds(
) -> None:

    grid = create_empty_grid()

    place_stones(grid, [(0, 0)], WHITE)
    place_stones(grid, [(0, 1), (0, 2)], BLACK)

    score = evaluate_captures(grid, 0, WHITE)

    assert score == STONE_CAPTURE


def test_no_capture_when_pattern_goes_out_of_bounds(
) -> None:

    grid = create_empty_grid()

    create_capture_configuration(
        grid,
        (9, 2),
        (0, -1),
        WHITE
    )

    score = evaluate_captures(grid, 0, WHITE)

    assert score == 0
