import pygame
from board import (
    STAR_POINTS,
    STAR_RADIUS
)
from board import (
    EMPTY,
    LINE_COLOR,
    NUMBER_OF_CELLS,
    STONE_RADIUS
)
from src.game.Board import Board
from src.game.Cell import Cell
from src.helpers.computation import intersection_to_pixel
from src.helpers.ui import get_stone_color
from window import (
    BOARD_MARGIN,
    CELL_SIZE,
    FORBIDDEN_COLOR,
    FORBIDDEN_RADIUS,
    PLAYGROUND_COLOR,
    PLAYGROUND_SIZE
)


def _draw_stars(
        screen: pygame.Surface
) -> None:

    for row, col in STAR_POINTS:
        pygame.draw.circle(
            screen,
            LINE_COLOR,
            intersection_to_pixel(row, col),
            STAR_RADIUS
        )


def _draw_forbidden_cells(
        screen: pygame.Surface,
        forbidden: list[tuple[int, int]]
) -> None:

    for row, col in forbidden:
        pygame.draw.circle(
            screen,
            FORBIDDEN_COLOR,
            intersection_to_pixel(row, col),
            FORBIDDEN_RADIUS
        )


def _draw_grid(
        screen: pygame.Surface,
        forbidden: list[tuple[int, int]]
) -> None:

    last = BOARD_MARGIN + (NUMBER_OF_CELLS - 1) * CELL_SIZE

    for i in range(NUMBER_OF_CELLS):
        offset = BOARD_MARGIN + i * CELL_SIZE
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (BOARD_MARGIN, offset),
            (last, offset)
        )
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (offset, BOARD_MARGIN),
            (offset, last)
        )

    _draw_stars(screen)
    _draw_forbidden_cells(screen, forbidden)


def draw_stone(
        screen: pygame.Surface,
        row: int,
        col: int,
        player: int
) -> None:

    center = intersection_to_pixel(row, col)
    color = get_stone_color(player)

    pygame.draw.circle(screen, color, center, STONE_RADIUS)
    pygame.draw.circle(screen, LINE_COLOR, center, STONE_RADIUS, 1)


def _draw_stones(
        screen: pygame.Surface,
        board: Board
) -> None:

    for row in range(NUMBER_OF_CELLS):
        for col in range(NUMBER_OF_CELLS):
            player = board.get_cell_state(Cell(row, col))
            if player != EMPTY:
                draw_stone(screen, row, col, player)


def draw_board(
        screen: pygame.Surface,
        board: Board,
        forbidden: list[tuple[int, int]]
) -> None:

    screen.fill(PLAYGROUND_COLOR, (0, 0, PLAYGROUND_SIZE, PLAYGROUND_SIZE))

    _draw_grid(screen, forbidden)
    _draw_stones(screen, board)


def draw_ghost(
        screen: pygame.Surface,
        ghost: pygame.Surface,
        row: int,
        col: int
) -> None:

    x, y = intersection_to_pixel(row, col)
    screen.blit(ghost, (x - STONE_RADIUS, y - STONE_RADIUS))
