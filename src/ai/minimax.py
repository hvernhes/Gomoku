"""Minimax avec elagage alpha-beta : choisit le coup du joueur courant."""
import random

from board import (
    EMPTY,
    NUMBER_OF_CELLS
)
from src.ai.candidates import candidate_cells
from src.ai.heuristic import evaluation
from src.ai.move_ordering import order_moves
from src.ai.weights import HeuristicWeights
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
        weights: HeuristicWeights,
        ai_player: int
) -> float:
    """Note d'une position non terminale, du point de vue de `ai_player`
    (plus c'est grand, mieux c'est pour lui). Adaptateur vers l'heuristique,
    avec un tout petit hasard pour departager les coups a egalite."""

    score = evaluation(board.grid, weights, board.captures, ai_player)
    if score != score:
        score = 0.0
    score = max(-EVALUATION_LIMIT, min(EVALUATION_LIMIT, score))

    return score + random.random() * 0.01


def _empty_cells(
        board: Board
) -> list[Cell]:
    """Toutes les cases vides, sans tester la legalite : le double-three
    (couteux) n'est verifie qu'au moment d'essayer un coup. Sert de repli
    quand aucun candidat n'est jouable (voir _moves_to_try)."""

    return [
        Cell(row, col)
        for row in range(NUMBER_OF_CELLS)
        for col in range(NUMBER_OF_CELLS)
        if board.grid[row][col] == EMPTY
    ]


def _moves_to_try(
        board: Board
):
    """Coups legaux a essayer, un par un et dans l'ordre : d'abord les
    candidats ; si aucun n'est legal, toutes les cases vides (repli : sinon
    une liste de candidats entierement interdite serait prise pour 'aucun
    coup'). La legalite est testee seulement quand la boucle demande le coup
    suivant (le plateau est restaure entre deux coups)."""

    found = False
    for cell in order_moves(board, candidate_cells(board)):
        if board.is_legal(cell):
            found = True
            yield cell
    if found:
        return
    for cell in order_moves(board, _empty_cells(board)):
        if board.is_legal(cell):
            yield cell


def minimax(
        board: Board,
        weights: HeuristicWeights,
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
        return evaluate(board, weights, ai_player)

    maximizing = board.current_player == ai_player
    best = -float("inf") if maximizing else float("inf")
    tried = False
    for cell in _moves_to_try(board):
        tried = True
        board.play(cell)
        try:
            score = minimax(board, weights, depth - 1, ai_player, alpha, beta)
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
        return evaluate(board, weights, ai_player)

    return best


def best_move(
        board: Board,
        weights: HeuristicWeights,
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
    for cell in _moves_to_try(board):
        board.play(cell)
        try:
            score = minimax(board, weights, depth - 1, ai_player, alpha, float("inf"))
        finally:
            board.undo()
        if score > best_score:
            best_score = score
            best = cell
            alpha = best_score

    return best
