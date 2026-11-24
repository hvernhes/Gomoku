"""Minimax simple (sans elagage) : choisit le coup du joueur courant."""

import random

from Game.board import DRAW, opponent_of

# Note d'une victoire : bien plus grande que toute note d'evaluation.
WIN_SCORE = 1_000_000

DEFAULT_DEPTH = 2


def evaluate(board, ai_player):
    """Note d'une position non terminale, du point de vue de `ai_player`
    (plus c'est grand, mieux c'est pour lui).

    Version provisoire : difference de pierres capturees, plus un tout petit
    hasard pour departager les coups a egalite. C'est le point d'accroche
    de l'heuristique, a remplacer plus tard."""
    opponent = opponent_of(ai_player)
    difference = board.captures[ai_player] - board.captures[opponent]
    return difference + random.random() * 0.01


def minimax(board, depth, ai_player):
    """Note de la position courante pour `ai_player`, en explorant `depth`
    coups de plus. L'IA maximise, son adversaire minimise."""
    # Positions terminales : notes exactes. On ajoute la profondeur restante
    # pour preferer une victoire proche (et retarder une defaite).
    result = board.result()
    if result == DRAW:
        return 0
    if result is not None:
        if result == ai_player:
            return WIN_SCORE + depth
        return -(WIN_SCORE + depth)

    # Limite de profondeur : on estime au lieu de continuer.
    if depth == 0:
        return evaluate(board, ai_player)

    moves = board.legal_moves()
    if not moves:
        return evaluate(board, ai_player)

    maximizing = board.current_player == ai_player
    best = -float("inf") if maximizing else float("inf")
    for row, col in moves:
        board.play(row, col)
        score = minimax(board, depth - 1, ai_player)
        board.undo()
        if maximizing:
            best = max(best, score)
        else:
            best = min(best, score)
    return best


def best_move(board, depth=DEFAULT_DEPTH):
    """Meilleur coup (row, col) du joueur courant, ou None s'il n'a aucun
    coup legal. Le plateau est laisse exactement comme il etait."""
    if depth < 1:
        raise ValueError("depth must be at least 1")
    ai_player = board.current_player
    best_score = -float("inf")
    best = None
    for row, col in board.legal_moves():
        board.play(row, col)
        score = minimax(board, depth - 1, ai_player)
        board.undo()
        if score > best_score:
            best_score = score
            best = (row, col)
    return best
