import pygame
import sys
from board import WHITE
from src.game.GameState import GameState
from src.helpers.events import process_events
from src.helpers.initialisation import initialize_display
from src.ui.window import draw_all_window
from window import FPS

USAGE = "usage: python3 -m src.gomoku [--hotseat]"


def main(
        ai_player: int | None = WHITE
):
    """Lance la partie. ai_player = couleur jouee par l'IA, ou None pour un
    hotseat (deux humains)."""

    pygame.init()

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

        state.save_log()

    finally:
        pygame.quit()


if __name__ == "__main__":

    arguments = sys.argv[1:]
    if arguments == ["--hotseat"]:
        sys.exit(main(ai_player=None))
    if arguments:
        print(USAGE)
        sys.exit(2)
    sys.exit(main())
