from heuristic import (
    CENTRAL,
    CENTRAL_MEDIUM,
    CENTRAL_FAR
)
from board import NUMBER_OF_CELLS
from src.ai.player_situation import PlayerSituation
from src.game.Cell import Cell


def check_central_position(
        cell: Cell,
        player_situation: PlayerSituation
) -> None:

    if (
        CENTRAL_FAR <= cell.row <= NUMBER_OF_CELLS - 1 - CENTRAL_FAR
        and CENTRAL_FAR <= cell.column <= NUMBER_OF_CELLS - 1 - CENTRAL_FAR
    ):
        player_situation.central_position += 1

    if (
        CENTRAL_MEDIUM <= cell.row <= NUMBER_OF_CELLS - 1 - CENTRAL_MEDIUM
        and CENTRAL_MEDIUM <= cell.column <= NUMBER_OF_CELLS - 1 - CENTRAL_MEDIUM
    ):
        player_situation.central_position += 1

    if (
        CENTRAL <= cell.row <= NUMBER_OF_CELLS - 1 - CENTRAL
        and CENTRAL <= cell.column <= NUMBER_OF_CELLS - 1 - CENTRAL
    ):
        player_situation.central_position += 1
