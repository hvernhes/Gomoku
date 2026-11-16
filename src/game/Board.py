"""Plateau de Gomoku : grille 19x19, joueur courant, captures et historique."""
from board import (
    NUMBER_OF_CELLS,
    EMPTY,
    BLACK,
    WHITE,
    DIRECTIONS,
    AXES,
    ALIGN_TO_WIN,
    CAPTURES_TO_WIN
)
from src.game.Cell import Cell
from src.helpers.utils import (
    opponent_of,
    in_bounds
)


class Board:
    def __init__(
            self
    ) -> None:
        # grid[row][col] contient EMPTY, BLACK ou WHITE (indices de 0 a 18).
        # Une liste par ligne : [[EMPTY] * N] * N copierait la MEME ligne N fois.
        self.grid = [[EMPTY] * NUMBER_OF_CELLS for _ in range(NUMBER_OF_CELLS)]
        self.current_player = BLACK
        # Nombre de pierres capturees PAR chaque joueur (une paire = 2).
        self.captures = {BLACK: 0, WHITE: 0}
        # Pile des coups joues : le dernier element est le plus recent.
        # Chaque entree est (row, col, captured), captured = pierres retirees.
        self.history = []

    def play(
            self,
            cell: Cell
        ) -> None:
        if not self.is_legal(cell):
            return

        player = self.current_player
        self.grid[cell.row][cell.column] = player

        captured = self._capture_pairs(cell, player)
        self.captures[player] += len(captured)
        self.history.append((cell.row, cell.column, captured))

        self.current_player = opponent_of(player)

    def undo(
            self
        ) -> None:
        if not self.history:
            return

        row, col, captured = self.history.pop()

        # On redevient le joueur qui avait joue ce coup.
        player = opponent_of(self.current_player)
        self.current_player = player
        self.grid[row][col] = EMPTY
        # Les pierres retirees appartenaient a l'adversaire de ce joueur.
        for cell in captured:
            self.grid[cell.row][cell.column] = opponent_of(player)
        self.captures[player] -= len(captured)

    def get_cell_state(
            self,
            cell: Cell
    ) -> int:
        # Pas de verification : un indice negatif lirait l'autre bout de la
        # liste sans erreur. L'appelant doit tester in_bounds avant.
        return self.grid[cell.row][cell.column]

    def is_full(
            self
        ) -> bool:
        # Plus aucune intersection libre : match nul si personne n'a gagne
        # (le sujet n'en parle pas, choix du projet).
        return all(cell != EMPTY for line in self.grid for cell in line)

    def is_legal(
            self,
            cell: Cell
        ) -> bool:
        """Coup legal pour le joueur courant : dans le plateau, case libre,
        et pas un double-three (sauf s'il capture une paire)."""

        if not in_bounds(cell) or not self._is_free(cell):
            return False

        player = self.current_player
        # Exception du sujet : un double-three introduit par une capture
        # est autorise.
        if self._find_captured(cell, player):
            return True

        return self._count_free_threes(cell.row, cell.column, player) < 2

    def winner(self):
        """Renvoie BLACK, WHITE ou None (pas de vainqueur), a partir du
        dernier coup. Ne stocke rien : rien a defaire dans undo."""

        if not self.history:
            return None

        row, col, _ = self.history[-1]
        mover = self.grid[row][col]
        other = opponent_of(mover)

        # 1. 10 pierres capturees : la victoire par capture prime.
        if self.captures[mover] >= CAPTURES_TO_WIN:
            return mover

        # 2. Le 5 forme par l'adversaire au coup precedent est toujours la :
        # le joueur n'a pas su le casser (endgame capture).
        if len(self.history) >= 2:
            prev_row, prev_col, _ = self.history[-2]
            if (self.grid[prev_row][prev_col] == other
                    and self.has_five_through(prev_row, prev_col)):
                return other

        # 3. Le dernier coup forme un 5 que l'adversaire ne peut pas arreter.
        if (self.has_five_through(row, col)
                and not self._can_stop_five(row, col, mover)):
            return mover
        return None

    def _capture_pairs(
            self,
            cell: Cell,
            player: int
        ) -> list[Cell]:
        """Retire les paires adverses encadrees par la pierre posee en
        (row, col) et renvoie la liste des cases retirees."""

        captured = self._find_captured(cell, player)
        for cell in captured:
            self.grid[cell.row][cell.column] = EMPTY

        return captured

    def _find_captured(
            self,
            cell: Cell,
            player: int
        ) -> list[Cell]:
        """Cases que capturerait une pierre de `player` posee en (row, col),
        sans rien modifier. La case (row, col) elle-meme n'est pas lue."""

        opponent = opponent_of(player)
        captured = []
        for direction_row, direction_column in DIRECTIONS:
            end_row = cell.row + 3 * direction_row
            end_col = cell.column + 3 * direction_column
            # Ligne droite : si la 3e case est dans le plateau, les deux
            # premieres le sont aussi. Un seul test de limite par direction.
            end_cell = Cell(end_row, end_col)
            if not in_bounds(end_cell):
                continue

            first_cell = Cell(cell.row + direction_row, cell.column + direction_column)
            second_cell = Cell(cell.row + 2 * direction_row, cell.column + 2 * direction_column)
            if (self.get_cell_state(first_cell) == opponent
                    and self.get_cell_state(second_cell) == opponent
                    and self.get_cell_state(end_cell) == player):
                captured.append(first_cell)
                captured.append(second_cell)

        return captured

    def _count_free_threes(
            self,
            row,
            col,
            player
        ) -> int:
        """Nombre d'axes (sur 4) sur lesquels une pierre de `player` posee
        en (row, col) cree un free-three. La pierre est posee
        temporairement, puis retiree."""

        count = 0
        self.grid[row][col] = player
        try:
            for d_row, d_col in AXES:
                if self._has_free_three(row, col, d_row, d_col, player):
                    count += 1
        finally:
            self.grid[row][col] = EMPTY
        return count

    def _has_free_three(self, row, col, d_row, d_col, player):
        """Free-three = il existe une case vide e qui, remplie par `player`,
        donne un quatre ouvert contenant la pierre en (row, col) et e.
        Le quatre occupe 4 cases : e est a au plus 3 cases de la pierre."""

        for step in range(-3, 4):
            if step == 0:
                continue
            e_row = row + step * d_row
            e_col = col + step * d_col
            if not in_bounds(Cell(e_row, e_col)) or self.grid[e_row][e_col] != EMPTY:
                continue
            self.grid[e_row][e_col] = player
            try:
                back = self._run_length(row, col, -d_row, -d_col, player)
                ahead = self._run_length(row, col, d_row, d_col, player)
                # e doit faire partie de la ligne, qui doit avoir 4 pierres
                # exactement et ses deux bouts libres.
                if -back <= step <= ahead and 1 + back + ahead == 4:
                    previous_cell = Cell(row - (back + 1) * d_row, col - (back + 1) * d_col)
                    next_cell = Cell(row + (ahead + 1) * d_row, col + (ahead + 1) * d_col)
                    if (self._is_free(previous_cell)
                            and self._is_free(next_cell)):
                        return True
            finally:
                self.grid[e_row][e_col] = EMPTY
        return False

    def _is_free(
            self,
            cell: Cell
        ) -> bool:
        """Bout libre : dans le plateau et vide (un bord ou une pierre ferme)."""

        return in_bounds(cell) and self.get_cell_state(cell) == EMPTY

    def has_five_through(self, row, col):
        """La pierre en (row, col) fait-elle partie d'un alignement de 5 ou
        plus (sur l'un des 4 axes) ?"""
        player = self.grid[row][col]
        if player == EMPTY:
            return False
        for d_row, d_col in AXES:
            length = (1
                      + self._run_length(row, col, d_row, d_col, player)
                      + self._run_length(row, col, -d_row, -d_col, player))
            if length >= ALIGN_TO_WIN:
                return True
        return False

    def _run_length(self, row, col, d_row, d_col, player):
        """Nombre de pierres de `player` qui se suivent depuis (row, col)
        dans la direction donnee, sans compter (row, col)."""
        count = 0
        row += d_row
        col += d_col
        while in_bounds(Cell(row, col)) and self.grid[row][col] == player:
            count += 1
            row += d_row
            col += d_col
        return count

    def _can_stop_five(self, five_row, five_col, five_player):
        """L'adversaire peut-il, en un coup, casser le 5 par une capture ou
        atteindre 10 pierres capturees ? Simulation brute : on essaie chaque
        case libre (play puis undo). Appele seulement quand un 5 vient
        d'etre forme, donc rarement. Suppose que c'est a l'adversaire de jouer."""
        stopper = opponent_of(five_player)
        for row in range(NUMBER_OF_CELLS):
            for col in range(NUMBER_OF_CELLS):
                if not self.is_legal(Cell(row, col)):
                    continue
                self.play(Cell(row, col))
                captured = self.history[-1][2]
                stops = bool(captured) and (
                    self.captures[stopper] >= CAPTURES_TO_WIN
                    or not self.has_five_through(five_row, five_col))
                self.undo()
                if stops:
                    return True
        return False

    def __str__(
            self
    ) -> str:

        symbols = {
            EMPTY: ".",
            BLACK: "X",
            WHITE: "O"
        }

        return "\n".join(
            " ".join(symbols[cell] for cell in line) for line in self.grid
        )
