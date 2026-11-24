import random
from src.ai.weights import HeuristicWeights


def crossover(
        parent_a: HeuristicWeights,
        parent_b: HeuristicWeights
) -> HeuristicWeights:

    child = []

    for weight_a, weight_b in zip(parent_a, parent_b):

        if random.random() < 0.5:
            child.append(weight_a)
        else:
            child.append(weight_b)

    return child
