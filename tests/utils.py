from board import (
    NUMBER_OF_CELLS,
    EMPTY
)


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