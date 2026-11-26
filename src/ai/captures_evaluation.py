from board import (
    AXES,
    NUMBER_OF_CELLS,
    EMPTY
)
from src.ai.weights import HeuristicWeights
from src.game.Cell import Cell
from src.helpers.utils import (
    get_cell_state,
    in_bounds,
    opponent_of
)


def _evaluate_capture_count(
        captures: int,
        weights: HeuristicWeights
) -> int:

    scores = {
        0: 0,
        2: weights.capture_one,
        4: weights.capture_two,
        6: weights.capture_three,
        8: weights.capture_four,
        10: weights.capture_five
    }

    return scores[captures]


def _get_capture_possibilities(
        grid: list[list[int]],
        starting_cell: Cell,
        player: int
) -> int:

    count = 0

    opponent = opponent_of(player)
    signs = (-1, 1)
    for sign in signs:
        for direction in AXES:
            concerned_cells: list[Cell] = []
            for i in range(1, 4):
                cell = Cell(
                    starting_cell.row + i * sign * direction[0],
                    starting_cell.column + i * sign * direction[1]
                )
                if not in_bounds(cell):
                    break
                concerned_cells.append(cell)

            if not len(concerned_cells) == 3:
                continue

            cell_states: list[int] = []
            for cell in concerned_cells:
                cell_states.append(get_cell_state(grid, cell))

            if (
                cell_states[0] == opponent
                and cell_states[1] == opponent
                and cell_states[2] == EMPTY
            ):
                count += 1

    return count


def _evaluate_capture_opportunities(
        grid: list[list[int]],
        player: int,
        weights: HeuristicWeights
) -> int:

    possible_captures = 0
    for row in range(NUMBER_OF_CELLS):
        for column in range(NUMBER_OF_CELLS):
            cell = Cell(row, column)
            if get_cell_state(grid, cell) != player:
                continue

            possible_captures += _get_capture_possibilities(
                grid,
                cell,
                player
            )

    return possible_captures * weights.stone_capture


def evaluate_captures(
        grid: list[list[int]],
        captures: int,
        player: int,
        weights: HeuristicWeights
) -> int:

    score = 0

    score += _evaluate_capture_count(captures, weights)
    score += _evaluate_capture_opportunities(grid, player, weights)

    return score
