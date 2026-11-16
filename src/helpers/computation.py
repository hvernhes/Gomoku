from display import (
    CELL_SIZE,
    MARGIN,
    SNAP_DISTANCE
)
from board import NUMBER_OF_CELLS


def intersection_to_pixel(
        row: int,
        col: int
) -> int:
    """Position en pixels (x, y) d'une intersection (ligne, colonne)."""

    return MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE


def pixel_to_intersection(
        x: int,
        y: int
) -> tuple[int, int]:
    """Intersection (ligne, colonne) sous le point (x, y), ou None si le
    point est hors du plateau ou trop loin de toute intersection."""

    # Intersection la plus proche (division entiere : pas de cas limite).
    col = (x - MARGIN + CELL_SIZE // 2) // CELL_SIZE
    row = (y - MARGIN + CELL_SIZE // 2) // CELL_SIZE
    if not (0 <= row < NUMBER_OF_CELLS and 0 <= col < NUMBER_OF_CELLS):
        return None

    center_x, center_y = intersection_to_pixel(row, col)
    if (x - center_x) ** 2 + (y - center_y) ** 2 > SNAP_DISTANCE ** 2:
        return None

    return row, col
