from board import (
    BLACK_STONE_COLOR,
    WHITE_STONE_COLOR
)
from board import BLACK


def get_player_name(
        player: int
) -> str:

    return "Black" if player == BLACK else "White"


def get_stone_color(
        player: int
) -> tuple[int, int, int]:

    return BLACK_STONE_COLOR if player == BLACK else WHITE_STONE_COLOR
