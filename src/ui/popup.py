import pygame
from board import LINE_COLOR
from src.helpers.ui import get_player_name
from src.ui.button import draw_button
from src.ui.UILayout import UILayout
from window import (
    PLAYGROUND_SIZE,
    POPUP_COLOR,
    POPUP_HEIGHT,
    POPUP_TEXT_COLOR,
    POPUP_WIDTH
)


def _draw_popup_window(
        screen: pygame.surface,
        popup_rectangle: pygame.Rect,
        font: pygame.font.Font,
        result: str | int | None
) -> None:

    popup_rectangle.center = (PLAYGROUND_SIZE // 2, PLAYGROUND_SIZE // 2)
    pygame.draw.rect(screen, POPUP_COLOR, popup_rectangle, border_radius=12)
    pygame.draw.rect(screen, LINE_COLOR, popup_rectangle, 2, border_radius=12)

    title = "Draw" if result == "draw" else f"{get_player_name(result)} wins"
    label = font.render(title, True, POPUP_TEXT_COLOR)

    screen.blit(
        label,
        label.get_rect(
            center=(popup_rectangle.centerx, popup_rectangle.top + 60)
    ))


def _draw_buttons(
        screen: pygame.surface,
        layout: UILayout,
        font: pygame.font.Font
) -> None:

    draw_button(screen, font, layout.popup_undo_button, "Undo")
    draw_button(screen, font, layout.popup_restart_button, "Restart")


def draw_popup(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        overlay: pygame.Surface,
        result: int | str | None,
        layout: UILayout
) -> None:
    """Popup au milieu du plateau quand la partie est finie."""

    screen.blit(overlay, (0, 0))

    _draw_popup_window(screen, layout.popup_rectangle, fonts["big"], result)
    _draw_buttons(screen, layout, fonts["normal"])
