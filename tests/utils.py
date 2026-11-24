from board import (
    NUMBER_OF_CELLS,
    EMPTY
)
from src.helpers.utils import opponent_of


def create_empty_grid(
) -> list[list[int]]:

    return [
        [EMPTY] * NUMBER_OF_CELLS
        for _ in range(NUMBER_OF_CELLS)
    ]


def place_stones(
        grid: list[list[int]],
        cells: list[tuple[int, int]],
        player: int
) -> None:

    for row, column in cells:
        grid[row][column] = player


def create_line(
        start: tuple[int, int],
        direction: tuple[int, int],
        length: int
) -> list[tuple[int, int]]:

    return [
        (
            start[0] + i * direction[0],
            start[1] + i * direction[1]
        )
        for i in range(length)
    ]


def create_capture_configuration(
        grid: list[list[int]],
        starting_cell: tuple[int, int],
        direction: tuple[int, int],
        player: int
):

    opponent = opponent_of(player)

    place_stones(grid, [starting_cell], player)

    first_opponent_cell = (
        starting_cell[0] + direction[0],
        starting_cell[1] + direction[1]
    )
    opponent_cells = create_line(first_opponent_cell, direction, 2)
    place_stones(grid, opponent_cells, opponent)
