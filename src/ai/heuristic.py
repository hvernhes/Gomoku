from src.ai.alignment_evaluation import evaluate_alignments
from src.ai.captures_evaluation import evaluate_captures
from src.ai.central_position_evaluation import evaluate_center
from src.helpers.utils import opponent_of


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
