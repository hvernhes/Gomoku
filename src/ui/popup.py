import pygame
from display import (
    BUTTON_COLOR,
    LINE_COLOR,
    POPUP_COLOR,
    POPUP_TEXT_COLOR,
    TEXT_COLOR
)
from src.helpers.ui import get_player_name
from window import PLAYGROUND_SIZE


POPUP_RECT = pygame.Rect(0, 0, 380, 190)
POPUP_RECT.center = (PLAYGROUND_SIZE // 2, PLAYGROUND_SIZE // 2)
POPUP_UNDO = pygame.Rect(POPUP_RECT.left + 30, POPUP_RECT.bottom - 70, 150, 44)
POPUP_RESTART = pygame.Rect(POPUP_UNDO.right + 20, POPUP_UNDO.top, 150, 44)


def draw_button(
        screen: pygame.Surface,
        font: pygame.font.Font,
        rectangle: pygame.Rect,
        text: str
) -> None:

    pygame.draw.rect(screen, BUTTON_COLOR, rectangle, border_radius=6)
    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=rectangle.center))


def draw_popup(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        overlay,
        result: int | str
) -> None:
    """Popup au milieu du plateau quand la partie est finie."""

    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, POPUP_COLOR, POPUP_RECT, border_radius=12)
    pygame.draw.rect(screen, LINE_COLOR, POPUP_RECT, 2, border_radius=12)
    title = "Draw" if result == "draw" else f"{get_player_name(result)} wins"
    label = fonts["big"].render(title, True, POPUP_TEXT_COLOR)
    screen.blit(label, label.get_rect(center=(POPUP_RECT.centerx,
                                             POPUP_RECT.top + 60)))
    draw_button(screen, fonts["normal"], POPUP_UNDO, "Undo")
    draw_button(screen, fonts["normal"], POPUP_RESTART, "Restart")
