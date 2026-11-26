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
<<<<<<< HEAD
        layout: UILayout
=======
        layout: UILayout,
        ai_player: int | None,
        ai_times: list[float],
        thinking: bool
>>>>>>> origin/master
) -> None:

    draw_board(screen, board, forbidden)

<<<<<<< HEAD
    if result is None:
=======
    if result is None and not thinking:
>>>>>>> origin/master
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

<<<<<<< HEAD
    draw_panel(screen, fonts, board, result, layout)
=======
    draw_panel(
        screen,
        fonts,
        board,
        result,
        layout,
        ai_player,
        ai_times,
        thinking
    )
>>>>>>> origin/master

    if result is not None:
        draw_popup(screen, fonts, overlay, result, layout)
