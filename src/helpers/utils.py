from board import (
    BLACK,
    NUMBER_OF_CELLS,
    WHITE
)
from src.game.Cell import Cell


def opponent_of(
        player: int
) -> int:

    if player == BLACK:
        return WHITE
    return BLACK


def in_bounds(
        cell: Cell
) -> bool:

    return 0 <= cell.row < NUMBER_OF_CELLS \
        and 0 <= cell.column < NUMBER_OF_CELLS


def get_cell_state(
        grid: list[list[int]],
        cell: Cell
) -> int | None:

    if not in_bounds(cell):
        return None

    return grid[cell.row][cell.column]
