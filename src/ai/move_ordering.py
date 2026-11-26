"""Ordonnancement des coups : essayer les coups prometteurs d'abord, pour que
l'alpha-beta coupe plus tot. Utilise les poids de l'heuristique (constantes de
heuristic.py) mais calcule lui-meme les lignes qui passent par une case."""
from board import (
    AXES,
    DIRECTIONS,
    EMPTY,
    NUMBER_OF_CELLS
)
from heuristic import (
    CENTRAL,
    CENTRAL_FAR,
    CENTRAL_MEDIUM,
    FIVE_OPEN_STONES,
    FOUR_BLOCKED_STONES,
    FOUR_HALF_BLOCKED_STONES,
    FOUR_OPEN_STONES,
    STONE_CAPTURE,
    THREE_BLOCKED_STONES,
    THREE_HALF_BLOCKED_STONES,
    THREE_OPEN_STONES
)
from src.game.Board import Board
from src.game.Cell import Cell
from src.helpers.utils import opponent_of


def _center_bonus(
        cell: Cell
) -> int:
    """Meme regle que evaluate_center (central_position_evaluation.py), pour
    une seule case."""

    last = NUMBER_OF_CELLS - 1
    bonus = 0
    for margin in (CENTRAL_FAR, CENTRAL_MEDIUM, CENTRAL):
        if (
            margin <= cell.row <= last - margin
            and margin <= cell.column <= last - margin
        ):
            bonus += 1

    return bonus


def _line_score(
        length: int,
        open_ends: int
) -> float:
    """Meme echelle de poids que l'heuristique (_compute_alignment_score),
    pour une ligne continue de `length` pierres dont `open_ends` bouts sont
    libres (0, 1 ou 2)."""

    if length >= 5:
        return FIVE_OPEN_STONES
    if length == 4:
        if open_ends == 2:
            return FOUR_OPEN_STONES
        if open_ends == 1:
            return FOUR_HALF_BLOCKED_STONES
        return FOUR_BLOCKED_STONES
    if length == 3:
        if open_ends == 2:
            return THREE_OPEN_STONES
        if open_ends == 1:
            return THREE_HALF_BLOCKED_STONES
        return THREE_BLOCKED_STONES

    return 0


def _stone_value(
        board: Board,
        cell: Cell,
        player: int
) -> float:
    """Ce qu'une pierre de `player` posee en `cell` lui rapporterait : les
    lignes continues qu'elle formerait sur les 4 axes, plus les captures
    immediates. Rien n'est joue ni modifie."""

    value = 0
    for d_row, d_col in AXES:
        back = board._run_length(cell.row, cell.column, -d_row, -d_col, player)
        ahead = board._run_length(cell.row, cell.column, d_row, d_col, player)
        before = Cell(
            cell.row - (back + 1) * d_row,
            cell.column - (back + 1) * d_col
        )
        after = Cell(
            cell.row + (ahead + 1) * d_row,
            cell.column + (ahead + 1) * d_col
        )
        open_ends = board._is_free(before) + board._is_free(after)
        value += _line_score(1 + back + ahead, open_ends)

    pairs = len(board._find_captured(cell, player)) // 2

    return value + pairs * STONE_CAPTURE


def _has_neighbor(
        board: Board,
        cell: Cell
) -> bool:
    """Vrai si l'une des 8 cases voisines est occupee (par l'un ou l'autre
    joueur). Sinon, aucune ligne de 3 ni capture n'est possible autour de la
    case."""

    for d_row, d_col in DIRECTIONS:
        row = cell.row + d_row
        col = cell.column + d_col
        if (
            0 <= row < NUMBER_OF_CELLS
            and 0 <= col < NUMBER_OF_CELLS
            and board.grid[row][col] != EMPTY
        ):
            return True

    return False


def score_move(
        board: Board,
        cell: Cell
) -> float:
    """Note rapide d'un coup pour le joueur courant : ce qu'il lui rapporte,
    plus ce qu'il retire a l'adversaire (qui y gagnerait autant)."""

    center = _center_bonus(cell)
    if not _has_neighbor(board, cell):
        # Aucune voisine occupee : _stone_value vaudrait exactement 0 pour
        # les deux joueurs, il ne reste que le bonus de centre.
        return center

    player = board.current_player

    return (
        _stone_value(board, cell, player)
        + _stone_value(board, cell, opponent_of(player))
        + center
    )


def order_moves(
        board: Board,
        moves: list[Cell]
) -> list[Cell]:
    """Les memes coups, du plus prometteur au moins prometteur. Le tri est
    stable : a note egale, l'ordre de legal_moves est conserve."""

    return sorted(moves, key=lambda cell: score_move(board, cell), reverse=True)
