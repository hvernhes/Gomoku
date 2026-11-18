from heuristic import (
    FIVE_OPEN_STONES,
    FOUR_BLOCKED_STONES,
    FOUR_OPEN_STONES,
    THREE_BLOCKED_STONES,
    THREE_OPEN_STONES
)
from board import (
    AXES,
    NUMBER_OF_CELLS,
    EMPTY
)
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
) -> tuple[set[tuple[int, int]], bool, bool, bool]:

    cells = set({(starting_cell.row, starting_cell.column)})
    empty = False
    free = False
    blocked = False

    for i in range(1, 5):
        adjacent_cell = Cell(
            starting_cell.row + i * direction[0],
            starting_cell.column + i * direction[1]
        )
        state = get_cell_state(grid, adjacent_cell)

        if state == player:
            cells.add((adjacent_cell.row, adjacent_cell.column))

        elif state is None or state == opponent:
            break

        elif state == EMPTY:
            second_adjacent_cell = Cell(
                adjacent_cell.row + direction[0],
                adjacent_cell.column + direction[1]
            )
            state = get_cell_state(grid, second_adjacent_cell)
            if state == EMPTY:
                free = True
                break
            if not empty:
                empty = True
            else:
                free = True
                break

    return (cells, empty, free, blocked)


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
    if next_cell_state != player:
        return (-1, True)

    opposite_cell = Cell(
        starting_cell.row - direction[0],
        starting_cell.column - direction[1]
    )
    opposite_cell_state = get_cell_state(grid, opposite_cell)
    if opposite_cell_state == EMPTY:
        return (1, True)
    elif opposite_cell_state != player:
        return (1, False)

    return (0, False)


def _add_alignment(
        alignment: dict[frozenset[tuple[int, int]], dict[str, bool]],
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int, int],
        player: int,
        opponent: int,
        received_free: bool
) -> None:

    cells, hole, free, blocked = _get_alignment_properties(
        grid,
        starting_cell,
        direction,
        player,
        opponent
    )

    if len(cells) >= 3:
        alignment[frozenset(cells)] = {
            "hole": hole,
            "free": received_free and free,
            "blocked": blocked
        }


def _handle_blocked_adjacent_cell(
        alignment: dict[frozenset[tuple[int, int]], dict[str, bool]],
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
        received_free=False
    )


def _handle_empty_adjacent_cell(
        alignment: dict[frozenset[tuple[int, int]], dict[str, bool]],
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int, int],
        player: int,
        opponent: int,
) -> None:

    sign, free = _start_of_alignment(grid, starting_cell, direction, player)

    if (sign != 0):
        good_direction = (direction[0] * sign, direction[1] * sign)
        _add_alignment(
            alignment,
            grid,
            starting_cell,
            good_direction,
            player,
            opponent,
            received_free=free
        )


def _handle_same_player_adjacent_cell(
        alignment: dict[frozenset[tuple[int, int]], dict[str, bool]],
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
            received_free=False
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
                received_free=True
            )


def _get_alignment(
        grid: list[list[int]],
        starting_cell: Cell,
        player: int
) -> dict[frozenset[tuple[int, int]], dict[str, bool]]:

    alignment: dict[frozenset[tuple[int, int]], dict[str, bool]] = {}
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


    print(alignment)
    return alignment


def _compute_alignment_score(
        aligned: list[dict[tuple, dict[str, bool]]]
) -> int:

    score = 0

    for cells, properties in aligned.items():
        if len(cells) >= 5:
            score += FIVE_OPEN_STONES

        elif len(cells) == 4:
            if properties["free"]:
                score += FOUR_OPEN_STONES
            else:
                score += FOUR_BLOCKED_STONES
        elif len(cells) == 3:
            if properties["free"]:
                score += THREE_OPEN_STONES
            else:
                score += THREE_BLOCKED_STONES

    return score


def evaluate_alignments(
        grid: list[list[int]],
        player: int
) -> int:

    aligned: dict[frozenset[tuple[int, int]], dict[str, bool]] = {}

    for row in range(NUMBER_OF_CELLS):
        for column in range(NUMBER_OF_CELLS):
            cell = Cell(row, column)

            if get_cell_state(grid, cell) != player:
                continue

            alignment = _get_alignment(
                grid,
                cell,
                player
            )
            for cells, properties in alignment.items():
                if cells not in aligned:
                    aligned[cells] = properties.copy()

    score = _compute_alignment_score(aligned)

    return score
