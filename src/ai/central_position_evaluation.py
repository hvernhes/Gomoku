from heuristic import (
    CENTRAL,
    CENTRAL_MEDIUM,
    CENTRAL_FAR
)
from board import NUMBER_OF_CELLS
from src.ai.player_situation import PlayerSituation
from src.game.Cell import Cell


CENTRAL_POSITION_SCORES = [
    [
        int(CENTRAL_FAR <= row <= NUMBER_OF_CELLS - 1 - CENTRAL_FAR
            and CENTRAL_FAR <= column <= NUMBER_OF_CELLS - 1 - CENTRAL_FAR)
        + int(CENTRAL_MEDIUM <= row <= NUMBER_OF_CELLS - 1 - CENTRAL_MEDIUM
            and CENTRAL_MEDIUM <= column <= NUMBER_OF_CELLS - 1 - CENTRAL_MEDIUM)
        + int(CENTRAL <= row <= NUMBER_OF_CELLS - 1 - CENTRAL
            and CENTRAL <= column <= NUMBER_OF_CELLS - 1 - CENTRAL)
        for column in range(NUMBER_OF_CELLS)
    ]
    for row in range(NUMBER_OF_CELLS)
]


def check_central_position(
        cell: tuple[int, int],
        player_situation: PlayerSituation
) -> None:

    player_situation.central_position += CENTRAL_POSITION_SCORES[cell[0]][cell[1]]
