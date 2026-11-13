import pygame
from board import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    EMPTY
)
from src.game.Board import Board
from window import (
    BOARD_SIZE,
    FPS,
    PANEL_COLOR,
    PANEL_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH
)


def compute_forbidden(board):
    """Intersections libres interdites au joueur courant (double-three).
    Calcule une fois par coup, pas a chaque image : c'est couteux."""
    return [(row, col)
            for row in range(BOARD_WIDTH)
            for col in range(BOARD_HEIGHT)
            if board.get_cell_state(row, col) == EMPTY and not board.is_legal(Cell(row, col))]


def draw_panel(screen, fonts, board, result):
    screen.fill(PANEL_COLOR, (BOARD_SIZE, 0, PANEL_WIDTH, BOARD_SIZE))
    draw_button(screen, fonts, UNDO_BUTTON, "Undo")

    # Tour de jeu : une pastille de la couleur du joueur, puis le texte.
    x = BOARD_PIXELS + 30
    if result is None:
        center = (x + 12, 145)
        pygame.draw.circle(screen, stone_color(board.current_player), center, 12)
        pygame.draw.circle(screen, TEXT_COLOR, center, 12, 1)
        text = f"{player_name(board.current_player)} to play"
    else:
        text = "Game over"
    label = fonts["normal"].render(text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(midleft=(x + 32, 145)))

    # Pierres capturees par chaque joueur (10 = victoire).
    title = fonts["normal"].render("Captures", True, TEXT_COLOR)
    screen.blit(title, (x, 210))
    for i, player in enumerate((BLACK, WHITE)):
        line = f"{player_name(player)}: {board.captures[player]} / {CAPTURES_TO_WIN}"
        label = fonts["small"].render(line, True, TEXT_COLOR)
        screen.blit(label, (x, 245 + 30 * i))


def main():

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Gomoku")
    clock = pygame.time.Clock()
    board = Board()
    forbidden = compute_forbidden(board)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(screen, board, forbidden)
        draw_panel(screen, fonts, board, result)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":

    main()
