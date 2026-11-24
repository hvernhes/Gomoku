from board import (
    EMPTY,
    NUMBER_OF_CELLS
)
from window import (
    CELL_SIZE,
    BOARD_MARGIN,
    SNAP_DISTANCE
)
from src.game.Cell import Cell


def intersection_to_pixel(
        row: int,
        col: int
) -> int:
    """Position en pixels (x, y) d'une intersection (ligne, colonne)."""

    return BOARD_MARGIN + col * CELL_SIZE, BOARD_MARGIN + row * CELL_SIZE


def pixel_to_intersection(
        x: int,
        y: int
) -> tuple[int, int]:
    """Intersection (ligne, colonne) sous le point (x, y), ou None si le
    point est hors du plateau ou trop loin de toute intersection."""

    # Intersection la plus proche (division entiere : pas de cas limite).
    col = (x - BOARD_MARGIN + CELL_SIZE // 2) // CELL_SIZE
    row = (y - BOARD_MARGIN + CELL_SIZE // 2) // CELL_SIZE
    if not (0 <= row < NUMBER_OF_CELLS and 0 <= col < NUMBER_OF_CELLS):
        return None

    center_x, center_y = intersection_to_pixel(row, col)
    if (x - center_x) ** 2 + (y - center_y) ** 2 > SNAP_DISTANCE ** 2:
        return None

    return row, col


def compute_forbidden(board):
    """Intersections libres interdites au joueur courant (double-three).
    Calcule une fois par coup, pas a chaque image : c'est couteux."""

    return [(row, col)
            for row in range(NUMBER_OF_CELLS)
            for col in range(NUMBER_OF_CELLS)
            if (
                board.get_cell_state(Cell(row, col)) == EMPTY
                and not board.is_legal(Cell(row, col))
            )]


def compute_result(board):
    """BLACK, WHITE, DRAW (plateau plein) ou None si la partie continue."""

    winner = board.winner()
    if winner is not None:
        return winner
    if board.is_full():
        return "draw"

    return None
