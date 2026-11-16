import pygame
from display import (
    PANEL_COLOR,
    PANEL_WIDTH,
    TEXT_COLOR
)
from board import (
    CAPTURES_TO_WIN,
    BLACK,
    WHITE
)
from src.game.Board import Board
from src.helpers.ui import (
    get_player_name,
    get_stone_color
)
from src.ui.popup import draw_button
from window import (
    MARGIN_SIZE,
    PLAYGROUND_SIZE,
    PANEL_COLOR,
    PANEL_WIDTH
)


UNDO_BUTTON = pygame.Rect(PLAYGROUND_SIZE + 30, 40, PANEL_WIDTH - 60, 44)


def _draw_player_to_play(
        x: int,
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        board: Board,
        result: str | int | None,
) -> None:

    if result is None:
        center = (x + 12, 145)
        pygame.draw.circle(screen, get_stone_color(board.current_player), center, 12)
        pygame.draw.circle(screen, TEXT_COLOR, center, 12, 1)
        text = f"{get_player_name(board.current_player)} to play"
    else:
        text = "Game over"

    label = fonts["normal"].render(text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(midleft=(x + 32, 145)))

    
def draw_panel(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        board: Board,
        result: str | int | None,
) -> None:

    screen.fill(PANEL_COLOR, (PLAYGROUND_SIZE, 0, PANEL_WIDTH, PLAYGROUND_SIZE))

    draw_button(screen, fonts["normal"], UNDO_BUTTON, "Undo")

    x = PLAYGROUND_SIZE + MARGIN_SIZE

    _draw_player_to_play(x, screen, fonts, board, result)

    # Pierres capturees par chaque joueur (10 = victoire).
    title = fonts["normal"].render("Captures", True, TEXT_COLOR)
    screen.blit(title, (x, 210))
    for i, player in enumerate((BLACK, WHITE)):
        line = f"{get_player_name(player)}: {board.captures[player]} / {CAPTURES_TO_WIN}"
        label = fonts["small"].render(line, True, TEXT_COLOR)
        screen.blit(label, (x, 245 + 30 * i))
