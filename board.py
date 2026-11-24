NUMBER_OF_CELLS = 19
STAR_POINTS = [(row, col) for row in (3, 9, 15) for col in (3, 9, 15)]
STAR_RADIUS = 5

STONE_RADIUS = 20
BOARD_COLOR = (222, 184, 135)
LINE_COLOR = (0, 0, 0)
BLACK_STONE_COLOR = (20, 20, 20)
WHITE_STONE_COLOR = (245, 245, 245)

EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
AXES = [
    (0, 1),
    (1, 0),
    (1, 1),
    (1, -1)
]

ALIGN_TO_WIN = 5
CAPTURES_TO_WIN = 10
