from src.ai.alignment_evaluation import evaluate_alignments
from src.ai.captures_evaluation import evaluate_captures
from src.ai.central_position_evaluation import evaluate_center
from src.helpers.utils import opponent_of


def evaluate_player(
        grid: list[list[int]],
        captures: int,
        player: int
) -> int:

    score = 0

    score += evaluate_alignments(grid, player)
    score += evaluate_captures(grid, captures, player)
    score += evaluate_center(grid, player)

    return score


def evaluation(
        grid: list[list[int]],
        captures: dict[int, int],
        player: int
) -> float:

    opponent = opponent_of(player)

    # if has_won(board, player):
    #     return WIN_SCORE

    # if has_won(board, opponent):
    #     return -WIN_SCORE

    player_score = evaluate_player(grid, captures[player], player)
    opponent_score = evaluate_player(grid, captures[opponent], opponent)

    return player_score - opponent_score
