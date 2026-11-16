from board import (
    NUMBER_OF_CELLS,
)


BIG_FONT = 64
NORMAL_FONT = 30
SMALL_FONT = 22

CELL_SIZE = 36            # ecart entre deux intersections (pixels)
MARGIN = 40          # marge autour de la grille
LAST = MARGIN + (NUMBER_OF_CELLS - 1) * CELL_SIZE        # coordonnee de la derniere ligne
BOARD_PIXELS = LAST + MARGIN                   # le plateau est un carre
PANEL_WIDTH = 240                              # panneau d'etat, a droite
WINDOW_SIZE = (BOARD_PIXELS + PANEL_WIDTH, BOARD_PIXELS)
STONE_RADIUS = 15
# Un clic (ou le survol) compte s'il tombe sur l'emplacement de la pierre.
SNAP_DISTANCE = STONE_RADIUS
FORBIDDEN_RADIUS = 6
FPS = 60

BOARD_COLOR = (222, 184, 135)
LINE_COLOR = (0, 0, 0)
PANEL_COLOR = (45, 45, 48)
TEXT_COLOR = (240, 240, 240)
BLACK_STONE_COLOR = (20, 20, 20)
WHITE_STONE_COLOR = (245, 245, 245)
RED = (200, 30, 30)
GHOST_ALPHA = 110    # transparence de l'apercu (0 = invisible, 255 = opaque)
BUTTON_COLOR = (90, 90, 96)
POPUP_COLOR = (245, 245, 245)
POPUP_TEXT_COLOR = (30, 30, 30)
OVERLAY_COLOR = (0, 0, 0, 120)
