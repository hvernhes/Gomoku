import pygame
import sys
from board import WHITE
from src.ai.heuristic import evaluation
from src.game.Board import Board
from src.game.GameState import GameState
from src.game.Cell import Cell
from src.helpers.computation import (
    compute_forbidden,
    compute_result,
    pixel_to_intersection
)
from src.helpers.events import process_events
from src.helpers.initialisation import (
    initialize_display,
    iniatilze_game
)
from src.ui.UILayout import UILayout
from src.ui.window import draw_all_window
from window import FPS


USAGE = "usage: python3 -m src.gomoku [--hotseat]"


# def handle_click(
#         pos,
#         board,
#         result,
#         layout: UILayout
# ) -> tuple[Board, bool]:

#     changed = False

#     if result is None:
#         if layout.undo_panel_button.collidepoint(pos):
#             if board.history:
#                 board.undo()
#                 changed = True

#         cell = pixel_to_intersection(*pos)

#         if cell is not None:
#             cell = Cell(*cell)

#             if board.is_legal(cell):
#                 player = board.current_player
#                 board.play(cell)

#                 value = evaluation(board.grid, board.captures, player)
#                 print(value)

#                 changed = True

#     else:
#         if layout.popup_undo_button.collidepoint(pos):
#             if board.history:
#                 board.undo()
#                 changed = True
#         elif layout.popup_restart_button.collidepoint(pos):
#             board = Board()
#             changed = True

#     return board, changed


# def main():

#     pygame.init()

#     try:
#         screen, fonts, ghosts, overlay, clock, layout = initialize_display()
#         board, result, forbidden = iniatilze_game()

#         running = True
#         while running:
#             changed = False

#             for event in pygame.event.get():

#                 if event.type == pygame.QUIT:
#                     running = False

#                 elif (
#                     event.type == pygame.MOUSEBUTTONDOWN
#                     and event.button == 1
#                 ):
#                     board, changed = handle_click(
#                         event.pos,
#                         board,
#                         result,
#                         layout
#                     )

#             if changed:
#                 result = compute_result(board)
#                 forbidden = (
#                     []
#                     if result is not None
#                     else compute_forbidden(board)
#                 )

#             if not running:
#                 break

#             draw_all_window(
#                 screen,
#                 board,
#                 fonts,
#                 result,
#                 forbidden,
#                 ghosts,
#                 overlay,
#                 layout
#             )

#             pygame.display.flip()
#             clock.tick(FPS)

#     finally:


def main(
        ai_player: int | None = WHITE
):
    """Lance la partie. ai_player = couleur jouee par l'IA, ou None pour un
    hotseat (deux humains)."""

    pygame.init()
    state = None

    try:
        screen, fonts, ghosts, overlay, clock, layout = initialize_display()
        state = GameState.new(ai_player)

        running = True
        while running:
            running = process_events(state, layout)
            if not running:
                break

            thinking = state.is_ai_turn()

            draw_all_window(
                screen,
                state.board,
                fonts,
                state.result,
                state.forbidden,
                ghosts,
                overlay,
                layout,
                state.ai_player,
                state.ai_times,
                thinking
            )

            pygame.display.flip()

            # Le tour de l'IA vient apres l'affichage : la pierre de
            # l'humain et "AI thinking..." sont deja a l'ecran quand la
            # fenetre se fige.
            if thinking:
                state.play_ai_turn()

            clock.tick(FPS)

    finally:
        # Le journal est sauvegarde aussi si le programme plante.
        if state is not None:
            state.save_log()
        pygame.quit()


if __name__ == "__main__":

    arguments = sys.argv[1:]
    if arguments == ["--hotseat"]:
        sys.exit(main(ai_player=None))
    if arguments:
        print(USAGE)
        sys.exit(2)

    sys.exit(main())
