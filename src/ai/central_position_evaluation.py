from heuristic import (
    CENTRAL,
    CENTRAL_MEDIUM,
    CENTRAL_FAR
)
from board import NUMBER_OF_CELLS
from src.ai.weights import HeuristicWeights
from src.game.Cell import Cell
from src.helpers.utils import (
    get_cell_state
)


def evaluate_center(
        grid: list[list[int]],
        player: int,
        weights: HeuristicWeights
) -> int:

    value = 0
    for row in range(NUMBER_OF_CELLS):
        for column in range(NUMBER_OF_CELLS):
            cell = Cell(row, column)
            if get_cell_state(grid, cell) != player:
                continue

            if (
                CENTRAL_FAR <= row <= NUMBER_OF_CELLS - 1 - CENTRAL_FAR
                and CENTRAL_FAR <= column <= NUMBER_OF_CELLS - 1 - CENTRAL_FAR
            ):
                value += weights.central_position
            if (
                CENTRAL_MEDIUM <= row <= NUMBER_OF_CELLS - 1 - CENTRAL_MEDIUM
                and CENTRAL_MEDIUM <= column <= NUMBER_OF_CELLS - 1 - CENTRAL_MEDIUM
            ):
                value += weights.central_position
            if (
                CENTRAL <= row <= NUMBER_OF_CELLS - 1 - CENTRAL
                and CENTRAL <= column <= NUMBER_OF_CELLS - 1 - CENTRAL
            ):
                value += weights.central_position

    return value
