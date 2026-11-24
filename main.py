"""Point d'entree : python3 main.py [--hotseat]

Par defaut, l'humain joue Noir contre l'IA (Blanc).
Avec --hotseat : deux humains sur le meme ecran.

Ce fichier fait tourner une partie : il lit les clics, fait jouer l'humain
et l'IA, chronometre l'IA et demande a Game/gui.py de dessiner.
"""

import sys
import time

import pygame

from AI.minimax import best_move
from Game import gui
from Game.board import BLACK, DRAW, EMPTY, WHITE, Board
from Game.game_log import new_log_path, save_game_log

USAGE = "usage: python3 main.py [--hotseat]"


def is_ai_turn(board, ai_player, result):
    """C'est a l'IA de jouer : partie en cours et main a la couleur de l'IA
    (jamais en hotseat, ai_player vaut alors None)."""
    return (ai_player is not None and result is None
            and board.current_player == ai_player)


def undo_for_human(board, ai_player):
    """Annule le dernier coup ; si la main revient a l'IA, annule aussi son
    coup, pour que ce soit a l'humain de jouer (sinon l'IA rejouerait aussitot
    la meme chose)."""
    board.undo()
    if (ai_player is not None and board.current_player == ai_player
            and board.history):
        board.undo()


def run_game(ai_player):
    """Lance la partie. ai_player = couleur jouee par l'IA, ou None pour un
    hotseat (deux humains)."""
    pygame.init()
    screen = pygame.display.set_mode(gui.WINDOW_SIZE)
    pygame.display.set_caption("Gomoku")
    fonts = {
        "big": pygame.font.Font(None, 64),
        "normal": pygame.font.Font(None, 30),
        "small": pygame.font.Font(None, 26),
    }
    ghosts = {BLACK: gui.make_ghost(gui.BLACK_STONE_COLOR),
              WHITE: gui.make_ghost(gui.WHITE_STONE_COLOR)}
    red_ghost = gui.make_ghost(gui.RED)
    overlay = gui.make_overlay()
    clock = pygame.time.Clock()
    board = Board()
    result = None
    forbidden = board.forbidden_moves()
    ai_times = []        # duree de reflexion de l'IA a chaque coup (secondes)
    log_path = new_log_path()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                changed = False
                undo_clicked = (gui.UNDO_BUTTON.collidepoint(event.pos)
                                or (result is not None
                                    and gui.POPUP_UNDO.collidepoint(
                                        event.pos)))
                if undo_clicked:
                    if board.history:
                        undo_for_human(board, ai_player)
                        changed = True
                elif result is not None and gui.POPUP_RESTART.collidepoint(
                        event.pos):
                    # La partie finie est sauvegardee avant d'etre remplacee.
                    save_game_log(log_path, board, ai_player, ai_times)
                    board = Board()
                    ai_times = []
                    log_path = new_log_path()
                    changed = True
                elif (result is None
                        and not is_ai_turn(board, ai_player, result)):
                    cell = gui.pixel_to_intersection(*event.pos)
                    # On verifie la legalite avant d'appeler play.
                    if cell is not None and board.is_legal(*cell):
                        board.play(*cell)
                        changed = True
                if changed:
                    result = board.result()
                    # Cases interdites : inutile de les calculer pour l'IA.
                    if result is not None or is_ai_turn(board, ai_player,
                                                        result):
                        forbidden = []
                    else:
                        forbidden = board.forbidden_moves()

        thinking = is_ai_turn(board, ai_player, result)
        gui.draw_board(screen, board, forbidden)
        if result is None and not thinking:
            hovered = gui.pixel_to_intersection(*pygame.mouse.get_pos())
            if hovered is not None and board.get(*hovered) == EMPTY:
                if hovered in forbidden:
                    gui.draw_ghost(screen, red_ghost, *hovered)
                else:
                    gui.draw_ghost(screen, ghosts[board.current_player],
                                   *hovered)
        gui.draw_panel(screen, fonts, board, result, ai_player, ai_times,
                       thinking)
        if result is not None:
            gui.draw_popup(screen, fonts, overlay, result)
        pygame.display.flip()

        # Le tour de l'IA vient apres l'affichage : la pierre de l'humain et
        # "AI thinking..." sont deja a l'ecran quand la fenetre se fige.
        if thinking:
            start = time.perf_counter()
            move = best_move(board)
            ai_times.append(time.perf_counter() - start)
            if move is None:
                # Aucun coup legal alors que la partie n'est pas finie :
                # on la termine plutot que de reboucler sans fin.
                result = DRAW
            else:
                board.play(*move)
                result = board.result()
            forbidden = [] if result is not None else board.forbidden_moves()
        clock.tick(gui.FPS)
    save_game_log(log_path, board, ai_player, ai_times)
    pygame.quit()


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--hotseat"]:
        run_game(ai_player=None)
    elif not args:
        run_game(ai_player=WHITE)
    else:
        print(USAGE)
        sys.exit(2)
