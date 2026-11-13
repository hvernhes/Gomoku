from rules import (
    BLACK,
    BOARD_SIZE,
    WHITE
)
from src.game.Cell import Cell


def opponent_of(
        player: int
) -> int:

    if player == BLACK:
        return WHITE
    return BLACK


def in_bounds(
        cell: Cell
) -> bool:

    return 0 <= cell.row < BOARD_SIZE \
        and 0 <= cell.column < BOARD_SIZE
