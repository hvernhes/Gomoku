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
AXES = [
    (0, 1),
    (1, 0),
    (1, 1),
    (1, -1)
]

ALIGN_TO_WIN = 5
CAPTURES_TO_WIN = 10
