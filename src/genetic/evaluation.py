from src.ai.weights import HeuristicWeights
from src.game.Board import Board


def play_game(
        player1: HeuristicWeights,
        player2: HeuristicWeights
) -> str:

    board = Board()

    board.play(player1, player2)
    result = board.compute_result()

    if result == 1:
        return "loss"
    elif result == 2:
        return "win"

    return "draw"


def fitness(
        individual: HeuristicWeights,
        opponents: list[HeuristicWeights],
        number_of_games: int = 5
) -> int:

    wins = 0
    draws = 0
    losses = 0

    for opponent in opponents:
        for _ in range(number_of_games):
            result = play_game(opponent, individual)
            if result == "win":
                wins += 1
            elif result == "draw":
                draws += 1
            else:
                losses += 1

    total_games = wins + draws + losses

    return (wins + 0.5 * draws) / total_games
