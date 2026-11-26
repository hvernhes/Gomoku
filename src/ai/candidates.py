"""Coups candidats : la recherche n'essaie que les cases vides proches d'une
pierre. C'est une approximation (voir CANDIDATE_RADIUS), pas une optimisation
exacte comme le tri des coups."""
from board import (
    EMPTY,
    NUMBER_OF_CELLS
)
from src.game.Board import Board
from src.game.Cell import Cell

# Distance maximale (en carre) entre une case candidate et une pierre.
# 1 : environ 4 fois moins de positions que 2, et le meme coup sur les
# positions mesurees ; 2 voit en plus les coups "avec un trou" (X X . X).
CANDIDATE_RADIUS = 1

CENTER = NUMBER_OF_CELLS // 2


def candidate_cells(
        board: Board,
        radius: int = CANDIDATE_RADIUS
) -> list[Cell]:
    """Cases vides a distance <= radius d'une pierre (des deux couleurs).
    Plateau sans pierre : le centre. Rien n'est modifie."""

    last = NUMBER_OF_CELLS - 1
    has_stone = False
    marked = set()
    for row in range(NUMBER_OF_CELLS):
        for col in range(NUMBER_OF_CELLS):
            if board.grid[row][col] == EMPTY:
                continue
            has_stone = True
            # Le carre autour de la pierre, coupe aux bords du plateau.
            for r in range(max(0, row - radius), min(last, row + radius) + 1):
                for c in range(
                    max(0, col - radius), min(last, col + radius) + 1
                ):
                    if board.grid[r][c] == EMPTY:
                        marked.add((r, c))

    if not has_stone:
        return [Cell(CENTER, CENTER)]

    # Tri : meme ordre que _empty_cells (ligne par ligne), donc des
    # departages reproductibles d'une partie a l'autre.
    return [Cell(r, c) for r, c in sorted(marked)]
