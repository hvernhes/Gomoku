import pygame
from board import EMPTY
from src.game.Board import Board
from src.game.Cell import Cell
from src.helpers.computation import pixel_to_intersection
from src.ui.board import (
    draw_board,
    draw_ghost
)
from src.ui.panel import draw_panel
from src.ui.popup import draw_popup
from src.ui.UILayout import UILayout


def draw_all_window(
        screen: pygame.Surface,
        board: Board,
        fonts: dict[str, pygame.font.Font],
        result: str | int | None,
        forbidden: list[tuple[int, int]],
        ghosts: dict[str | int, pygame.Surface],
        overlay: pygame.Surface,
        layout: UILayout
) -> None:

    draw_board(screen, board, forbidden)

    if result is None:
        hovered = pixel_to_intersection(*pygame.mouse.get_pos())

        if hovered is not None:
            cell = Cell(*hovered)

            if board.get_cell_state(cell) == EMPTY:
                ghost = (
                    ghosts["RED"]
                    if hovered in forbidden
                    else ghosts[board.current_player]
                )

                draw_ghost(screen, ghost, *hovered)

    draw_panel(screen, fonts, board, result, layout)

    if result is not None:
        draw_popup(screen, fonts, overlay, result, layout)
