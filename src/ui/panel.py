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
        thinking: bool,
        x: int
) -> None:

    if result is None:
        center = (x + 12, 145)
        pygame.draw.circle(
            screen,
            get_stone_color(board.current_player),
            center,
            12
        )
        pygame.draw.circle(screen, TEXT_COLOR, center, 12, 1)
        if thinking:
            text = "AI thinking..."
        else:
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
        line = (
            f"{get_player_name(player)}: \
                {board.captures[player]} / {CAPTURES_TO_WIN}"
        )
        label = fonts["small"].render(line, True, TEXT_COLOR)
        screen.blit(label, (x, 245 + 30 * i))


def _draw_ai_time(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        ai_times: list[float],
        x: int
) -> None:
    """Temps de reflexion de l'IA : dernier coup et moyenne (le sujet exige
    une moyenne inferieure a 0,5 s)."""

    title = fonts["normal"].render("AI time", True, TEXT_COLOR)
    screen.blit(title, (x, 330))

    if ai_times:
        last = f"Last: {ai_times[-1]:.2f} s"
        average = f"Average: {sum(ai_times) / len(ai_times):.2f} s"
    else:
        last = "Last: -"
        average = "Average: -"

    for i, line in enumerate((last, average)):
        label = fonts["small"].render(line, True, TEXT_COLOR)
        screen.blit(label, (x, 365 + 30 * i))


def draw_panel(
        screen: pygame.Surface,
        fonts: dict[str, pygame.font.Font],
        board: Board,
        result: str | int | None,
        layout: UILayout,
        ai_player: int | None,
        ai_times: list[float],
        thinking: bool
) -> None:

    screen.fill(
        PANEL_COLOR,
        (PLAYGROUND_SIZE, 0, PANEL_WIDTH, PLAYGROUND_SIZE)
    )

    x = PLAYGROUND_SIZE + PANEL_MARGIN
    _draw_undo_button(screen, fonts["normal"], layout.undo_panel_button)
    _draw_player_to_play(screen, fonts["normal"], board, result, thinking, x)
    _draw_captures(screen, fonts, board, x)
    if ai_player is not None:
        _draw_ai_time(screen, fonts, ai_times, x)
