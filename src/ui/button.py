import pygame
from window import (
    BUTTON_COLOR,
    TEXT_COLOR
)


def draw_button(
        screen: pygame.Surface,
        font: pygame.font.Font,
        rectangle: pygame.Rect,
        text: str
) -> None:

    pygame.draw.rect(screen, BUTTON_COLOR, rectangle, border_radius=6)
    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=rectangle.center))
