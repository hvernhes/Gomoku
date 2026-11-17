from heuristic import (
    CENTRAL,
    CENTRAL_MEDIUM,
    CENTRAL_FAR,
    FIVE_OPEN_STONES,
    FOUR_BLOCKED_STONES,
    FOUR_OPEN_STONES,
    STONE_CAPTURE,
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
    opponent_of,
    in_bounds
)


def start_of_alignment(
        grid: list[list[int]],
        empty_cell: Cell,
        direction: tuple[int],
        opponent: int,
) -> int:

    next_cell = Cell(
        empty_cell.row + direction[0],
        empty_cell.column + direction[1]
    )
    state = get_cell_state(grid, next_cell)
    if state == opponent or state == EMPTY:
        return -1

    opposite_cell = Cell(
        empty_cell.row - direction[0] * 2,
        empty_cell.column - direction[1] * 2
    )
    state = get_cell_state(grid, opposite_cell)
    if state == opponent or state == EMPTY:
        return 1

    return 0


def get_alignment_properties(
        grid: list[list[int]],
        starting_cell: Cell,
        direction: tuple[int],
        player: int,
        opponent: int  
) -> tuple[set[tuple[int]], bool]:

    cells = set({(starting_cell.row, starting_cell.column)})

    empty = False
    for i in range(1, 5):
        adjacent_cell = Cell(
            starting_cell.row + i * direction[0],
            starting_cell.column + i * direction[1]
        )
        state = get_cell_state(grid, adjacent_cell)

        if state == player:
            cells.add((adjacent_cell.row, adjacent_cell.column))
        elif state == opponent:
            break
        elif state == EMPTY and not empty:
            empty = True
        elif state == EMPTY and empty:
            break

    return (cells, empty)


def start_of_alignment(
        grid: list[list[int]],
        empty_cell: Cell,
        direction: tuple[int],
        opponent: int,
) -> int:

    next_cell = Cell(
        empty_cell.row + direction[0],
        empty_cell.column + direction[1]
    )
    state = get_cell_state(grid, next_cell)
    if state == opponent or state == EMPTY:
        return -1

    opposite_cell = Cell(
        empty_cell.row - direction[0] * 2,
        empty_cell.column - direction[1] * 2
    )
    state = get_cell_state(grid, opposite_cell)
    if state == opponent or state == EMPTY:
        return 1

    return 0


def get_alignment(
        grid: list[list[int]],
        starting_cell: Cell,
        player: int
) -> dict[dict[str, bool]]:

    alignment: dict[dict[str, bool]] = {}

    opponent = opponent_of(player)
    for direction in AXES:
        adjacent_cell = Cell(
            starting_cell.row + direction[0],
            starting_cell.column + direction[1]
        )
        state = get_cell_state(grid, adjacent_cell)

        if state == opponent:
            opposite_direction = (-direction[0], -direction[1])
            cells, hole = get_alignment_properties(
                grid,
                starting_cell,
                opposite_direction,
                player,
                opponent
            )
            alignment[frozenset(cells)] = {
                "hole": hole,
                "free": False
            }

        elif state == EMPTY:
            if (sign := start_of_alignment(grid, adjacent_cell, direction, opponent)):
                good_direction = (direction[0] * sign, direction[1] * sign)     
                cells, hole = get_alignment_properties(
                    grid,
                    starting_cell,
                    good_direction,
                    player,
                    opponent
                )
                alignment[frozenset(cells)] = {
                    "hole": hole,
                    "free": True
                }

    return alignment
    

def compute_alignment_score(
        aligned: list[dict[tuple, dict[str, bool]]]
) -> int:

    score = 0

    for combo in aligned:
        for cells in combo:
            if len(cells) >= 5:
                score += FIVE_OPEN_STONES
            elif len(cells) == 4:
                if combo[cells]["free"]:
                    score += FOUR_OPEN_STONES
                else:
                    score += FOUR_BLOCKED_STONES
            elif len(cells) == 3:
                if combo[cells]["free"]:
                    score += THREE_OPEN_STONES
                else:
                    score += THREE_BLOCKED_STONES

    return score


def evaluate_alignments(
        grid: list[list[int]],
        player: int
) -> int:

    aligned: list[dict[tuple, dict[str, bool]]] = []
    for row in range(NUMBER_OF_CELLS):
        for column in range(NUMBER_OF_CELLS):
            cell = Cell(row, column)
            if get_cell_state(grid, cell) != player:
                continue

            alignment = get_alignment(
                grid,
                cell,
                player
            )
            if alignment:
                aligned.append(alignment)

    score = compute_alignment_score(aligned)

    return score


def get_capture_possibilities(
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

            cell_states: list[int] = []
            for cell in concerned_cells:
                cell_states.append(get_cell_state(grid, cell))

            if cell_states[0] == opponent \
                and cell_states[1] == opponent \
                and cell_states[2] == EMPTY:
                count += 1

    return count


def evaluate_captures(
        grid: list[list[int]],
        player: int
) -> int:

    possible_captures = 0
    for row in range(NUMBER_OF_CELLS):
        for column in range(NUMBER_OF_CELLS):
            cell = Cell(row, column)
            if get_cell_state(grid, cell) != player:
                continue

            possible_captures += get_capture_possibilities(
                grid,
                cell,
                player
            )

    score = possible_captures * STONE_CAPTURE

    return score


def is_empty_around(
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
            if not in_bounds(cell):
                return False

            adjacent_cell_state = get_cell_state(grid, adjacent_cell)
            if adjacent_cell_state != EMPTY:
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

            if is_empty_around(grid, cell):
                if CENTRAL_FAR <= row <= NUMBER_OF_CELLS - CENTRAL_FAR \
                    and CENTRAL_FAR <= column <= NUMBER_OF_CELLS - CENTRAL_FAR:
                    value += 1
                if CENTRAL_MEDIUM <= row <= NUMBER_OF_CELLS - CENTRAL_MEDIUM \
                    and CENTRAL_MEDIUM <= column <= NUMBER_OF_CELLS - CENTRAL_MEDIUM:
                    value += 1
                if CENTRAL <= row <= NUMBER_OF_CELLS - CENTRAL \
                    and CENTRAL <= column <= NUMBER_OF_CELLS - CENTRAL:
                    value += 1

    return value


def evaluate_player(
        grid: list[list[int]],
        player: int
) -> int:

    score = 0

    score += evaluate_alignments(grid, player)
    score += evaluate_captures(grid, player)
    score += evaluate_center(grid, player)

    return score


def evaluation(
        grid: list[list[int]],
        player: int
) -> float:
    """
    Ce qui rapporte des points:
        - free three in a row
        - half free four in a row
        - free four in a row
        - five in a row (-> presque victoire)
        - possibility of capture
        - possibility of capture (-> count 4)
        - possibility of capture (-> count 5) -> victoire

    five in a row, four in a row, three in a row, central cell, capture
    """

    opponent = opponent_of(player)

    # if has_won(board, player):
    #     return WIN_SCORE

    # if has_won(board, opponent):
    #     return -WIN_SCORE

    player_score = evaluate_player(grid, player)
    opponent_score = evaluate_player(grid, opponent)

    return player_score - opponent_score


def get_cell_state(
        grid: list[list[int]],
        cell: Cell
) -> int:
    # Pas de verification : un indice negatif lirait l'autre bout de la
    # liste sans erreur. L'appelant doit tester in_bounds avant.
    return grid[cell.row][cell.column]
