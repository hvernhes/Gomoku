from board import (
    AXES,
    EMPTY
)
from src.ai.player_situation import PlayerSituation
from src.game.Cell import Cell
from src.helpers.utils import (
    get_cell_state,
    in_bounds,
    opponent_of
)


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


def check_captures(
        grid: list[list[int]],
        cell: Cell,
        player: int,
        player_situation: PlayerSituation
) -> None:

    player_situation.captures["possible_captures"] += _get_capture_possibilities(
        grid,
        cell,
        player
    )
