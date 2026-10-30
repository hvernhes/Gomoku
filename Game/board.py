"""Plateau de Gomoku : grille 19x19, joueur courant, captures et historique."""

BOARD_SIZE = 19

EMPTY = 0
BLACK = 1
WHITE = 2

# Les 8 directions, sous forme de pas (ligne, colonne).
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


# Un axe = une direction et son opposee (horizontal, vertical, 2 diagonales).
AXES = [(0, 1), (1, 0), (1, 1), (1, -1)]

ALIGN_TO_WIN = 5
CAPTURES_TO_WIN = 10


def opponent_of(player):
    if player == BLACK:
        return WHITE
    return BLACK


class Board:
    def __init__(self):
        # grid[row][col] contient EMPTY, BLACK ou WHITE (indices de 0 a 18).
        # Une liste par ligne : [[EMPTY] * N] * N copierait la MEME ligne N fois.
        self.grid = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = BLACK
        # Nombre de pierres capturees PAR chaque joueur (une paire = 2).
        self.captures = {BLACK: 0, WHITE: 0}
        # Pile des coups joues : le dernier element est le plus recent.
        # Chaque entree est (row, col, captured), captured = pierres retirees.
        self.history = []

    def in_bounds(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def get(self, row, col):
        # Pas de verification : un indice negatif lirait l'autre bout de la
        # liste sans erreur. L'appelant doit tester in_bounds avant.
        return self.grid[row][col]

    def is_full(self):
        """Plus aucune intersection libre : match nul si personne n'a gagne
        (le sujet n'en parle pas, choix du projet)."""
        return all(cell != EMPTY for line in self.grid for cell in line)

    def is_legal(self, row, col):
        """Coup legal pour le joueur courant : dans le plateau, case libre,
        et pas un double-three (sauf s'il capture une paire)."""
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return False
        player = self.current_player
        # Exception du sujet : un double-three introduit par une capture
        # est autorise.
        if self._find_captured(row, col, player):
            return True
        return self._count_free_threes(row, col, player) < 2

    def play(self, row, col):
        if not self.is_legal(row, col):
            raise ValueError(f"illegal move: ({row}, {col})")
        player = self.current_player
        self.grid[row][col] = player
        captured = self._capture_pairs(row, col, player)
        self.captures[player] += len(captured)
        self.history.append((row, col, captured))
        self.current_player = opponent_of(player)

    def undo(self):
        if not self.history:
            raise ValueError("nothing to undo")
        row, col, captured = self.history.pop()
        # On redevient le joueur qui avait joue ce coup.
        player = opponent_of(self.current_player)
        self.current_player = player
        self.grid[row][col] = EMPTY
        # Les pierres retirees appartenaient a l'adversaire de ce joueur.
        for cap_row, cap_col in captured:
            self.grid[cap_row][cap_col] = opponent_of(player)
        self.captures[player] -= len(captured)

    def _capture_pairs(self, row, col, player):
        """Retire les paires adverses encadrees par la pierre posee en
        (row, col) et renvoie la liste des cases retirees."""
        captured = self._find_captured(row, col, player)
        for cap_row, cap_col in captured:
            self.grid[cap_row][cap_col] = EMPTY
        return captured

    def _find_captured(self, row, col, player):
        """Cases que capturerait une pierre de `player` posee en (row, col),
        sans rien modifier. La case (row, col) elle-meme n'est pas lue."""
        opponent = opponent_of(player)
        captured = []
        for d_row, d_col in DIRECTIONS:
            end_row = row + 3 * d_row
            end_col = col + 3 * d_col
            # Ligne droite : si la 3e case est dans le plateau, les deux
            # premieres le sont aussi. Un seul test de limite par direction.
            if not self.in_bounds(end_row, end_col):
                continue
            row1, col1 = row + d_row, col + d_col
            row2, col2 = row + 2 * d_row, col + 2 * d_col
            if (self.grid[row1][col1] == opponent
                    and self.grid[row2][col2] == opponent
                    and self.grid[end_row][end_col] == player):
                captured.append((row1, col1))
                captured.append((row2, col2))
        return captured

    def _count_free_threes(self, row, col, player):
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
            if not self.in_bounds(e_row, e_col) or self.grid[e_row][e_col] != EMPTY:
                continue
            self.grid[e_row][e_col] = player
            try:
                back = self._run_length(row, col, -d_row, -d_col, player)
                ahead = self._run_length(row, col, d_row, d_col, player)
                # e doit faire partie de la ligne, qui doit avoir 4 pierres
                # exactement et ses deux bouts libres.
                if -back <= step <= ahead and 1 + back + ahead == 4:
                    before_row = row - (back + 1) * d_row
                    before_col = col - (back + 1) * d_col
                    after_row = row + (ahead + 1) * d_row
                    after_col = col + (ahead + 1) * d_col
                    if (self._is_free(before_row, before_col)
                            and self._is_free(after_row, after_col)):
                        return True
            finally:
                self.grid[e_row][e_col] = EMPTY
        return False

    def _is_free(self, row, col):
        """Bout libre : dans le plateau et vide (un bord ou une pierre ferme)."""
        return self.in_bounds(row, col) and self.grid[row][col] == EMPTY

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
        while self.in_bounds(row, col) and self.grid[row][col] == player:
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
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self.is_legal(row, col):
                    continue
                self.play(row, col)
                captured = self.history[-1][2]
                stops = bool(captured) and (
                    self.captures[stopper] >= CAPTURES_TO_WIN
                    or not self.has_five_through(five_row, five_col))
                self.undo()
                if stops:
                    return True
        return False

    def __str__(self):
        symbols = {EMPTY: ".", BLACK: "X", WHITE: "O"}
        return "\n".join(
            " ".join(symbols[cell] for cell in line) for line in self.grid
        )
