import pygame
from board import (
    BLACK,
    BLACK_STONE_COLOR,
    LINE_COLOR,
    STONE_RADIUS,
    WHITE,
    WHITE_STONE_COLOR
)
from src.game.Board import Board
from src.helpers.computation import compute_forbidden
from src.ui.UILayout import UILayout
from window import (
    BIG_FONT,
    FORBIDDEN_COLOR,
    GHOST_ALPHA,
    NORMAL_FONT,
    OVERLAY_COLOR,
    PANEL_MARGIN,
    PANEL_WIDTH,
    PLAYGROUND_SIZE,
    POPUP_HEIGHT,
    POPUP_WIDTH,
    SMALL_FONT,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH
)


def _open_window(
        window_width,
        window_height,
        window_title
) -> pygame.Surface:

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(window_title)

    return screen


def _make_ghost(color):
    """Pierre semi-transparente de la couleur donnee (creee une fois)."""

    size = 2 * STONE_RADIUS
    ghost = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (STONE_RADIUS, STONE_RADIUS)
    pygame.draw.circle(ghost, (*color, GHOST_ALPHA), center, STONE_RADIUS)
    pygame.draw.circle(ghost, (*LINE_COLOR, GHOST_ALPHA), center,
                       STONE_RADIUS, 1)

    return ghost


def _make_overlay():
    overlay = pygame.Surface((PLAYGROUND_SIZE, PLAYGROUND_SIZE), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    return overlay


def _initialize_ui_layout(
) -> UILayout:

    undo_panel_button = pygame.Rect(PLAYGROUND_SIZE + PANEL_MARGIN, PANEL_MARGIN, PANEL_WIDTH - PANEL_MARGIN * 2, 50)
    popup_rectangle = pygame.Rect(0, 0, POPUP_WIDTH, POPUP_HEIGHT)
    popup_rectangle.center = (
        PLAYGROUND_SIZE // 2,
        PLAYGROUND_SIZE // 2
    )
    popup_undo_button = pygame.Rect(popup_rectangle.left + 30, popup_rectangle.bottom - 70, 150, 44)
    popup_restart_button = pygame.Rect(popup_undo_button.right + 20, popup_undo_button.top, 150, 44)

    return UILayout(
        undo_panel_button,
        popup_rectangle,
        popup_undo_button,
        popup_restart_button
    )


def initialize_display(
) -> tuple[
    pygame.Surface,
    dict[str, pygame.font.Font],
    dict[int | str, pygame.Surface],
    pygame.Surface,
    pygame.Clock,
    UILayout
]:

    screen = _open_window(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        WINDOW_TITLE
    )

    fonts = {
        "big": pygame.font.Font(None, BIG_FONT),
        "normal": pygame.font.Font(None, NORMAL_FONT),
        "small": pygame.font.Font(None, SMALL_FONT),
    }
    ghosts = {
        BLACK: _make_ghost(BLACK_STONE_COLOR),
        WHITE: _make_ghost(WHITE_STONE_COLOR),
        "RED": _make_ghost(FORBIDDEN_COLOR)
    }
    overlay = _make_overlay()
    clock = pygame.time.Clock()

    ui_layout = _initialize_ui_layout()

    return screen, fonts, ghosts, overlay, clock, ui_layout


def iniatilze_game(
) -> tuple[Board, None | str | int, list[tuple[int, int]]]:

    board = Board()
    result = None
    forbidden = compute_forbidden(board)

    return board, result, forbidden