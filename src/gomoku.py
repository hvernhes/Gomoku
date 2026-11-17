import pygame
import sys
from src.ai.heuristic import evaluation
from src.game.Board import Board
from src.game.Cell import Cell
from src.helpers.computation import (
    compute_forbidden,
    compute_result,
    pixel_to_intersection
)
from src.helpers.initialisation import (
    initialize_display,
    iniatilze_game
)
from src.ui.UILayout import UILayout
from src.ui.window import draw_all_window
from window import FPS


def handle_click(
        pos,
        board,
        result,
        layout: UILayout
) -> tuple[Board, bool]:

    changed = False

    if result is None:
        if layout.undo_panel_button.collidepoint(pos):
            if board.history:
                board.undo()
                changed = True

        cell = pixel_to_intersection(*pos)

        if cell is not None:
            cell = Cell(*cell)

            if board.is_legal(cell):
                player = board.current_player
                board.play(cell)

                value = evaluation(board.grid, player)
                print(value)

                changed = True

    else:
        if layout.popup_undo_button.collidepoint(pos):
            if board.history:
                board.undo()
                changed = True
        elif layout.popup_restart_button.collidepoint(pos):
            board = Board()
            changed = True

    return board, changed


def main():

    pygame.init()

    try:
        screen, fonts, ghosts, overlay, clock, layout = initialize_display()
        board, result, forbidden = iniatilze_game()

        running = True
        while running:
            changed = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    board, changed = handle_click(
                        event.pos,
                        board,
                        result,
                        layout
                    )

            if changed:
                result = compute_result(board)
                forbidden = (
                    []
                    if result is not None
                    else compute_forbidden(board)
                )

            if not running:
                break

            draw_all_window(
                screen,
                board,
                fonts,
                result,
                forbidden,
                ghosts,
                overlay,
                layout
            )

            pygame.display.flip()
            clock.tick(FPS)

    finally:
        pygame.quit()


if __name__ == "__main__":

    sys.exit(main())
