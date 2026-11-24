from src.ai.weights import HeuristicWeights


def select_bests(
        individuals: list[HeuristicWeights],
        strenghts: list[float]
) -> list[HeuristicWeights]:

    ranked = sorted(
        zip(strenghts, individuals),
        key=lambda item: item[0],
        reverse=True
    )

    return [
        individual
        for _, individual in ranked[:len(individuals) // 2]
    ]
