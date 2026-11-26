"""Minimax avec elagage alpha-beta : choisit le coup du joueur courant."""
import random

from board import (
    EMPTY,
    NUMBER_OF_CELLS
)
from src.ai.heuristic import evaluation
from src.ai.move_ordering import order_moves
from src.game.Board import Board
from src.game.Cell import Cell
from src.helpers.computation import compute_result
from src.helpers.utils import opponent_of

# Note d'une victoire : bien plus grande que toute note d'evaluation.
WIN_SCORE = 1_000_000
# L'heuristique peut renvoyer une valeur infinie (constantes en np.inf) ou
# nan (inf - inf) : on borne sa note pour qu'une vraie victoire l'emporte
# toujours et que min / max restent fiables.
EVALUATION_LIMIT = WIN_SCORE // 2

DEFAULT_DEPTH = 2


def evaluate(
        board: Board,
        ai_player: int
) -> float:
    """Note d'une position non terminale, du point de vue de `ai_player`
    (plus c'est grand, mieux c'est pour lui). Adaptateur vers l'heuristique,
    avec un tout petit hasard pour departager les coups a egalite."""

    score = evaluation(board.grid, board.captures, ai_player)
    if score != score:
        score = 0.0
    score = max(-EVALUATION_LIMIT, min(EVALUATION_LIMIT, score))

    return score + random.random() * 0.01


def _empty_cells(
        board: Board
) -> list[Cell]:
    """Toutes les cases vides, sans tester la legalite : le double-three
    (couteux) n'est verifie qu'au moment d'essayer un coup."""

    return [
        Cell(row, col)
        for row in range(NUMBER_OF_CELLS)
        for col in range(NUMBER_OF_CELLS)
        if board.grid[row][col] == EMPTY
    ]


def minimax(
        board: Board,
        depth: int,
        ai_player: int,
        alpha: float = -float("inf"),
        beta: float = float("inf")
) -> float:
    """Note de la position courante pour `ai_player`, en explorant `depth`
    coups de plus. L'IA maximise, son adversaire minimise.
    alpha : note que l'IA est deja sure d'obtenir ; beta : note que
    l'adversaire laissera au plus. Des que beta <= alpha, le reste du noeud
    ne peut plus changer la decision : on coupe."""

    # Positions terminales : notes exactes. On ajoute la profondeur restante
    # pour preferer une victoire proche (et retarder une defaite).
    result = compute_result(board)
    if result == "draw":
        return 0
    if result is not None:
        if result == ai_player:
            return WIN_SCORE + depth
        return -(WIN_SCORE + depth)

    # Limite de profondeur : on estime au lieu de continuer.
    if depth == 0:
        return evaluate(board, ai_player)

    maximizing = board.current_player == ai_player
    best = -float("inf") if maximizing else float("inf")
    tried = False
    for cell in order_moves(board, _empty_cells(board)):
        if not board.is_legal(cell):
            continue
        tried = True
        board.play(cell)
        try:
            score = minimax(board, depth - 1, ai_player, alpha, beta)
        finally:
            # Meme si la recherche plante, le coup simule est annule.
            board.undo()
        if maximizing:
            best = max(best, score)
            alpha = max(alpha, best)
        else:
            best = min(best, score)
            beta = min(beta, best)
        if beta <= alpha:
            break

    # Aucun coup legal alors que la partie n'est pas finie (cas quasi
    # impossible) : on estime la position au lieu de renvoyer l'infini.
    if not tried:
        return evaluate(board, ai_player)

    return best


def best_move(
        board: Board,
        depth: int = DEFAULT_DEPTH
) -> Cell | None:
    """Meilleur coup du joueur courant, ou None s'il n'a aucun coup legal.
    Le plateau est laisse exactement comme il etait."""

    if depth < 1:
        raise ValueError("depth must be at least 1")

    ai_player = board.current_player
    alpha = -float("inf")
    best_score = -float("inf")
    best = None
    for cell in order_moves(board, _empty_cells(board)):
        if not board.is_legal(cell):
            continue
        board.play(cell)
        try:
            score = minimax(board, depth - 1, ai_player, alpha, float("inf"))
        finally:
            board.undo()
        if score > best_score:
            best_score = score
            best = cell
            alpha = best_score

    return best
