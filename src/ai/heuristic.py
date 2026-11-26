from board import NUMBER_OF_CELLS
from src.ai.alignment_evaluation import check_alignment
from src.ai.captures_evaluation import check_captures
from src.ai.central_position_evaluation import check_central_position
from src.ai.player_situation import (
    init_player_situation,
    PlayerSituation
)
from src.ai.weights import HeuristicWeights
from src.game.Cell import Cell
from src.helpers.utils import (
    get_cell_state,
    opponent_of
)


def player_evaluation(
        player: int,
        grid: list[list[int]],
        cell: Cell,
        player_situation: PlayerSituation
) -> None:

    check_alignment(grid, cell, player, player_situation)
    check_captures(grid, cell, player, player_situation)
    check_central_position(cell, player_situation)


def evaluate_alignments(
        aligned: dict[frozenset[tuple[int, int]], dict[str, bool | int]],
        weights: HeuristicWeights
) -> int:

    score = 0

    for cells, properties in aligned.items():
        if len(cells) >= 5 and not properties["broken"]:
            score += weights.five_open_stones

        elif len(cells) >= 4:
            if properties["free"] == 2 and not properties["broken"]:
                score += weights.four_open_stones
            elif properties["free"] == 1 or properties["broken"] or len(cells) >= 5:          
                score += weights.four_half_blocked_stones
            else:
                score += weights.four_blocked_stones

        elif len(cells) == 3:
            if properties["free"] == 2:
                score += weights.three_open_stones
            elif properties["free"] == 1:          
                score += weights.three_half_blocked_stones
            else:
                score += weights.three_blocked_stones

    return score


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
    }

    return scores.get(captures)


def compute_captures(
        possible_captures: int,
        weights: HeuristicWeights
) -> int:

    return possible_captures * weights.stone_capture


def compute_player_score(
        player_situation: PlayerSituation,
        weights: HeuristicWeights
) -> int:

    score = 0

    score += evaluate_alignments(player_situation.aligned, weights)

    score += _evaluate_capture_count(player_situation.captures["captured_stones"], weights)
    score += compute_captures(player_situation.captures["possible_captures"], weights)

    score += player_situation.central_position * weights.central_position

    return score


def evaluation(
        grid: list[list[int]],
        weights: HeuristicWeights,
        captures: dict[int, int],
        player: int
) -> float:

    opponent = opponent_of(player)

    current_player_situation = init_player_situation(captures[player])
    opponent_situation = init_player_situation(captures[opponent])

    for row in range(NUMBER_OF_CELLS):
        for column in range(NUMBER_OF_CELLS):

            if grid[row][column] == player:
                player_evaluation(player, grid, Cell(row, column), current_player_situation)
            elif grid[row][column] == opponent:
                player_evaluation(opponent, grid, Cell(row, column), opponent_situation)

    player_score = compute_player_score(current_player_situation, weights)
    opponent_score = compute_player_score(opponent_situation, weights)

    return player_score - opponent_score
