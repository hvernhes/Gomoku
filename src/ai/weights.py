from dataclasses import dataclass
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
    CAPTURE_FIVE,
    STONE_CAPTURE,
    CENTRAL_POSITION
)


@dataclass
class HeuristicWeights:
        three_blocked_stones: int
        three_half_blocked_stones: int
        three_open_stones: int
        four_blocked_stones: int
        four_half_blocked_stones: int
        four_open_stones: int
        five_open_stones: int
        capture_one: int
        capture_two: int
        capture_three: int
        capture_four: int
        capture_five: int
        stone_capture: int
        central_position: int


def generate_weights(
) -> HeuristicWeights:

    return HeuristicWeights(
        three_blocked_stones=THREE_BLOCKED_STONES,
        three_half_blocked_stones=THREE_HALF_BLOCKED_STONES,
        three_open_stones=THREE_OPEN_STONES,
        four_blocked_stones=FOUR_BLOCKED_STONES,
        four_half_blocked_stones=FOUR_HALF_BLOCKED_STONES,
        four_open_stones=FOUR_OPEN_STONES,
        five_open_stones=FIVE_OPEN_STONES,
        capture_one=CAPTURE_ONE,
        capture_two=CAPTURE_TWO,
        capture_three=CAPTURE_THREE,
        capture_four=CAPTURE_FOUR,
        capture_five=CAPTURE_FIVE,
        stone_capture=STONE_CAPTURE,
        central_position=CENTRAL_POSITION
    )