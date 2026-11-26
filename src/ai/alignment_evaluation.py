from board import (
    AXES,
    EMPTY
)
from src.ai.player_situation import PlayerSituation
from src.game.Cell import Cell
from src.helpers.utils import (
    get_cell_state,
    opponent_of
)


def _get_alignment_properties(
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int, int],
        player: int,
        opponent: int
) -> tuple[set[tuple[int, int]], bool, bool]:

    cells = set({(starting_cell.row, starting_cell.column)})
    empty = False
    second_blocked_end = False

    for i in range(1, 6):
        adjacent_cell = Cell(
            starting_cell.row + i * direction[0],
            starting_cell.column + i * direction[1]
        )
        state = get_cell_state(grid, adjacent_cell)

        if state == player:
            cells.add((adjacent_cell.row, adjacent_cell.column))

        elif state is None or state == opponent:
            second_blocked_end = True
            break

        elif state == EMPTY:
            second_adjacent_cell = Cell(
                adjacent_cell.row + direction[0],
                adjacent_cell.column + direction[1]
            )
            second_adjacent_cell_state = get_cell_state(grid, second_adjacent_cell)
            if second_adjacent_cell_state == EMPTY:
                break
            if not empty:
                empty = True
            else:
                break

    return (cells, empty, second_blocked_end)


def _start_of_alignment(
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int, int],
        player: int
) -> tuple[int, bool]:

    next_cell = Cell(
        starting_cell.row + direction[0] * 2,
        starting_cell.column + direction[1] * 2
    )
    next_cell_state = get_cell_state(grid, next_cell)

    if next_cell_state == EMPTY:
        return (-1, False)
    elif next_cell_state != player:
        return (-1, True)

    opposite_cell = Cell(
        starting_cell.row - direction[0],
        starting_cell.column - direction[1]
    )
    opposite_cell_state = get_cell_state(grid, opposite_cell)
    if opposite_cell_state == EMPTY:
        return (1, False)
    elif opposite_cell_state != player:
        return (1, True)

    return (0, True)


def _add_alignment(
        alignment: dict[frozenset[tuple[int, int]], dict[str, bool | int]],
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int, int],
        player: int,
        opponent: int,
        first_end_blocked: bool
) -> None:

    cells, hole, second_end_blocked = _get_alignment_properties(
        grid,
        starting_cell,
        direction,
        player,
        opponent
    )

    if len(cells) >= 3:
        alignment[frozenset(cells)] = {
            "broken": hole,
            "free": 2 - first_end_blocked - second_end_blocked
        }


def _handle_blocked_adjacent_cell(
        alignment: dict[frozenset[tuple[int, int]], dict[str, bool | int]],
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int, int],
        player: int,
        opponent: int,
) -> None:

    opposite_direction = (-direction[0], -direction[1])
    _add_alignment(
        alignment,
        grid,
        starting_cell,
        opposite_direction,
        player,
        opponent,
        first_end_blocked=True
    )


def _handle_empty_adjacent_cell(
        alignment: dict[frozenset[tuple[int, int]], dict[str, bool | int]],
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int, int],
        player: int,
        opponent: int,
) -> None:

    sign, blocked = _start_of_alignment(grid, starting_cell, direction, player)

    if (sign != 0):
        good_direction = (direction[0] * sign, direction[1] * sign)
        _add_alignment(
            alignment,
            grid,
            starting_cell,
            good_direction,
            player,
            opponent,
            first_end_blocked=blocked
        )


def _handle_same_player_adjacent_cell(
        alignment: dict[frozenset[tuple[int, int]], dict[str, bool | int]],
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int, int],
        player: int,
        opponent: int,
) -> None:

    opposite_direction = (-direction[0], -direction[1])
    opposite_cell = Cell(
        starting_cell.row + opposite_direction[0],
        starting_cell.column + opposite_direction[1]
    )
    opposite_cell_state = get_cell_state(grid, opposite_cell)

    if opposite_cell_state == opponent or opposite_cell_state is None:
        _add_alignment(
            alignment,
            grid,
            starting_cell,
            direction,
            player,
            opponent,
            first_end_blocked=True
        )

    elif opposite_cell_state == EMPTY:
        second_opposite_cell = Cell(
            starting_cell.row + opposite_direction[0] * 2,
            starting_cell.column + opposite_direction[1] * 2
        )
        second_opposite_cell_state =  get_cell_state(grid, second_opposite_cell)

        if second_opposite_cell_state != player:
            _add_alignment(
                alignment,
                grid,
                starting_cell,
                direction,
                player,
                opponent,
                first_end_blocked=False
            )


def _get_alignment(
        grid: list[list[int]],
        starting_cell: Cell,
        player: int
) -> dict[frozenset[tuple[int, int]], dict[str, bool | int]]:

    alignment: dict[frozenset[tuple[int, int]], dict[str, bool | int]] = {}
    opponent = opponent_of(player)

    for direction in AXES:

        adjacent_cell = Cell(
            starting_cell.row + direction[0],
            starting_cell.column + direction[1]
        )
        adjacent_cell_state = get_cell_state(grid, adjacent_cell)

        if adjacent_cell_state == opponent or adjacent_cell_state is None:
            _handle_blocked_adjacent_cell(
                alignment,
                grid,
                starting_cell,
                direction,
                player,
                opponent,
            )

        elif adjacent_cell_state == EMPTY:
            _handle_empty_adjacent_cell(
                alignment,
                grid,
                starting_cell,
                direction,
                player,
                opponent,
            )

        elif adjacent_cell_state == player:
            _handle_same_player_adjacent_cell(
                alignment,
                grid,
                starting_cell,
                direction,
                player,
                opponent,
            )

    return alignment


def check_alignment(
        grid: list[list[int]],
        cell: Cell,
        player: int,
        player_situation: PlayerSituation
) -> None:

    alignment = _get_alignment(
        grid,
        cell,
        player
    )

    for cells, properties in alignment.items():
        if cells not in player_situation.aligned:
            player_situation.aligned[cells] = properties.copy()
