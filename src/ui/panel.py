import pygame
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
from src.ui.button import draw_button
from src.ui.popup import draw_button
from src.ui.UILayout import UILayout
from window import (
    PLAYGROUND_SIZE,
    PANEL_COLOR,
    PANEL_MARGIN,
    PANEL_WIDTH,
    TEXT_COLOR
)


def _draw_undo_button(
        screen: pygame.Surface,
        font: pygame.font.Font,
        undo_panel_button: pygame.Rect
) -> None:

    draw_button(
        screen,
        font,
        undo_panel_button,
        "Undo"
    )


def _draw_player_to_play(
        screen: pygame.Surface,
        font: pygame.font.Font,
        board: Board,
        result: str | int | None,
        x: int
) -> None:

    if result is None:
        center = (x + 12, 145)
        pygame.draw.circle(screen, get_stone_color(board.current_player), center, 12)
        pygame.draw.circle(screen, TEXT_COLOR, center, 12, 1)
        text = f"{get_player_name(board.current_player)} to play"
    else:
        text = "Game over"

    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(midleft=(x + 32, 145)))


def _draw_captures(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        board: Board,
        x: int
) -> None:

    title = fonts["normal"].render("Captures", True, TEXT_COLOR)
    screen.blit(title, (x, 210))
    for i, player in enumerate((BLACK, WHITE)):
        line = f"{get_player_name(player)}: {board.captures[player]} / {CAPTURES_TO_WIN}"
        label = fonts["small"].render(line, True, TEXT_COLOR)
        screen.blit(label, (x, 245 + 30 * i))


def draw_panel(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        board: Board,
        result: str | int | None,
        layout: UILayout
) -> None:

    screen.fill(PANEL_COLOR, (PLAYGROUND_SIZE, 0, PANEL_WIDTH, PLAYGROUND_SIZE))

    x = PLAYGROUND_SIZE + PANEL_MARGIN
    _draw_undo_button(screen, fonts["normal"], layout.undo_panel_button)
    _draw_player_to_play(screen, fonts["normal"], board, result, x)
    _draw_captures(screen, fonts, board, x)
