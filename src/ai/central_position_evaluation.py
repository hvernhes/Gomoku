from heuristic import (
    CENTRAL,
    CENTRAL_MEDIUM,
    CENTRAL_FAR
)
from board import (
    AXES,
    NUMBER_OF_CELLS,
    EMPTY
)
from src.game.Cell import Cell
from src.helpers.utils import (
    get_cell_state
)


def _is_empty_around(
        grid: list[list[int]],
        cell: Cell
) -> bool:

    signs = (-1, 1)
    for sign in signs:
        for direction in AXES:
            adjacent_cell = Cell(
                cell.row + sign * direction[0],
                cell.column + sign * direction[1]
            )
            adjacent_cell_state = get_cell_state(grid, adjacent_cell)
            if (
                adjacent_cell_state is None
                or adjacent_cell_state != EMPTY
            ):
                return False

    return True


def evaluate_center(
        grid: list[list[int]],
        player: int
) -> int:

    value = 0
    for row in range(NUMBER_OF_CELLS):
        for column in range(NUMBER_OF_CELLS):
            cell = Cell(row, column)
            if get_cell_state(grid, cell) != player:
                continue

            if _is_empty_around(grid, cell):
                if (
                    CENTRAL_FAR <= row <= NUMBER_OF_CELLS - CENTRAL_FAR
                    and CENTRAL_FAR <= column <= NUMBER_OF_CELLS - CENTRAL_FAR
                ):
                    value += 1
                if (
                    CENTRAL_MEDIUM <= row <= NUMBER_OF_CELLS - CENTRAL_MEDIUM
                    and CENTRAL_MEDIUM <= column <= NUMBER_OF_CELLS - CENTRAL_MEDIUM
                ):
                    value += 1
                if (
                    CENTRAL <= row <= NUMBER_OF_CELLS - CENTRAL
                    and CENTRAL <= column <= NUMBER_OF_CELLS - CENTRAL
                ):
                    value += 1

    return value
