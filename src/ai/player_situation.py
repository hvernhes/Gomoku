from dataclasses import dataclass


@dataclass
class PlayerSituation:
    aligned: dict[frozenset[tuple[int, int]], dict[str, bool | int]]
    captures: dict[str, int]
    central_position: dict[str, int]


def init_player_situation(
        captured_stones
) -> PlayerSituation:

    return PlayerSituation(
        aligned={},
        captures={
            "possible_captures": 0,
            "captured_stones": captured_stones
        },
        central_position=0
    )
