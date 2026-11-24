import random
import numpy as np
from src.ai.weights import HeuristicWeights
from heuristic import (
    THREE_BLOCKED_STONES,
    THREE_HALF_BLOCKED_STONES,
    THREE_OPEN_STONES,
    FOUR_BLOCKED_STONES,
    FOUR_HALF_BLOCKED_STONES,
    FOUR_OPEN_STONES,
    FIVE_OPEN_STONES,
    CAPTURE_ONE,
    CAPTURE_TWO,
    CAPTURE_THREE,
    CAPTURE_FOUR,
    STONE_CAPTURE,
    CENTRAL_POSITION
)




def _generate_individual(
) -> HeuristicWeights:

    return HeuristicWeights(
        three_blocked_stones=random.randint(0, THREE_BLOCKED_STONES),
        three_half_blocked_stones=random.randint(0, THREE_HALF_BLOCKED_STONES),
        three_open_stones=random.randint(0, THREE_OPEN_STONES),
        four_blocked_stones=random.randint(0, FOUR_BLOCKED_STONES),
        four_half_blocked_stones=random.randint(0, FOUR_HALF_BLOCKED_STONES),
        four_open_stones=random.randint(0, FOUR_OPEN_STONES),
        five_open_stones=random.randint(0, FIVE_OPEN_STONES),
        capture_one=random.randint(0, CAPTURE_ONE),
        capture_two=random.randint(0, CAPTURE_TWO),
        capture_three=random.randint(0, CAPTURE_THREE),
        capture_four=random.randint(0, CAPTURE_FOUR),
        capture_five=np.inf,
        stone_capture=random.randint(0, STONE_CAPTURE),
        central_position=random.randint(0, CENTRAL_POSITION),
    )


def generate_population(
        population_size: int
) -> list[HeuristicWeights]:

    return [
        _generate_individual() for _ in range(population_size)
    ]
