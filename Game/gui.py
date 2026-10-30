"""Interface graphique (pygame-ce) : plateau de Gomoku jouable en hotseat."""

import pygame

from board import (BLACK, BOARD_SIZE, CAPTURES_TO_WIN, EMPTY, WHITE, Board)

CELL = 36            # ecart entre deux intersections (pixels)
MARGIN = 40          # marge autour de la grille
LAST = MARGIN + (BOARD_SIZE - 1) * CELL        # coordonnee de la derniere ligne
BOARD_PIXELS = LAST + MARGIN                   # le plateau est un carre
PANEL_WIDTH = 240                              # panneau d'etat, a droite
WINDOW_SIZE = (BOARD_PIXELS + PANEL_WIDTH, BOARD_PIXELS)
STONE_RADIUS = 15
# Un clic (ou le survol) compte s'il tombe sur l'emplacement de la pierre.
SNAP_DISTANCE = STONE_RADIUS
STAR_RADIUS = 4
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

UNDO_BUTTON = pygame.Rect(BOARD_PIXELS + 30, 40, PANEL_WIDTH - 60, 44)
POPUP_RECT = pygame.Rect(0, 0, 380, 190)
POPUP_RECT.center = (BOARD_PIXELS // 2, BOARD_PIXELS // 2)
# Deux boutons en bas de la popup : Undo (annuler le dernier coup) et
# Restart (nouvelle partie).
POPUP_UNDO = pygame.Rect(POPUP_RECT.left + 30, POPUP_RECT.bottom - 70, 150, 44)
POPUP_RESTART = pygame.Rect(POPUP_UNDO.right + 20, POPUP_UNDO.top, 150, 44)

DRAW = "draw"        # resultat : match nul (plateau plein, pas de vainqueur)

# Les 9 points reperes d'un goban 19x19, en (ligne, colonne).
STAR_POINTS = [(row, col) for row in (3, 9, 15) for col in (3, 9, 15)]


def intersection_to_pixel(row, col):
    """Position en pixels (x, y) d'une intersection (ligne, colonne)."""
    return MARGIN + col * CELL, MARGIN + row * CELL


def pixel_to_intersection(x, y):
    """Intersection (ligne, colonne) sous le point (x, y), ou None si le
    point est hors du plateau ou trop loin de toute intersection."""
    # Intersection la plus proche (division entiere : pas de cas limite).
    col = (x - MARGIN + CELL // 2) // CELL
    row = (y - MARGIN + CELL // 2) // CELL
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return None
    center_x, center_y = intersection_to_pixel(row, col)
    if (x - center_x) ** 2 + (y - center_y) ** 2 > SNAP_DISTANCE ** 2:
        return None
    return row, col


def compute_result(board):
    """BLACK, WHITE, DRAW (plateau plein) ou None si la partie continue."""
    winner = board.winner()
    if winner is not None:
        return winner
    if board.is_full():
        return DRAW
    return None


def compute_forbidden(board):
    """Intersections libres interdites au joueur courant (double-three).
    Calcule une fois par coup, pas a chaque image : c'est couteux."""
    return [(row, col)
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
            if board.get(row, col) == EMPTY and not board.is_legal(row, col)]


def stone_color(player):
    return BLACK_STONE_COLOR if player == BLACK else WHITE_STONE_COLOR


def player_name(player):
    return "Black" if player == BLACK else "White"


def draw_stone(screen, row, col, player):
    center = intersection_to_pixel(row, col)
    pygame.draw.circle(screen, stone_color(player), center, STONE_RADIUS)
    pygame.draw.circle(screen, LINE_COLOR, center, STONE_RADIUS, 1)


def make_ghost(color):
    """Pierre semi-transparente de la couleur donnee (creee une fois)."""
    size = 2 * STONE_RADIUS
    ghost = pygame.Surface((size, size), pygame.SRCALPHA)
    center = (STONE_RADIUS, STONE_RADIUS)
    pygame.draw.circle(ghost, (*color, GHOST_ALPHA), center, STONE_RADIUS)
    pygame.draw.circle(ghost, (*LINE_COLOR, GHOST_ALPHA), center,
                       STONE_RADIUS, 1)
    return ghost


def draw_ghost(screen, ghost, row, col):
    x, y = intersection_to_pixel(row, col)
    screen.blit(ghost, (x - STONE_RADIUS, y - STONE_RADIUS))


def draw_board(screen, board, forbidden):
    screen.fill(BOARD_COLOR, (0, 0, BOARD_PIXELS, BOARD_PIXELS))
    for i in range(BOARD_SIZE):
        offset = MARGIN + i * CELL
        pygame.draw.line(screen, LINE_COLOR, (MARGIN, offset), (LAST, offset))
        pygame.draw.line(screen, LINE_COLOR, (offset, MARGIN), (offset, LAST))
    for row, col in STAR_POINTS:
        pygame.draw.circle(screen, LINE_COLOR,
                           intersection_to_pixel(row, col), STAR_RADIUS)
    for row, col in forbidden:
        pygame.draw.circle(screen, RED, intersection_to_pixel(row, col),
                           FORBIDDEN_RADIUS)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            player = board.get(row, col)
            if player != EMPTY:
                draw_stone(screen, row, col, player)


def draw_button(screen, fonts, rect, text):
    pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=6)
    label = fonts["normal"].render(text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=rect.center))


def draw_panel(screen, fonts, board, result):
    screen.fill(PANEL_COLOR, (BOARD_PIXELS, 0, PANEL_WIDTH, BOARD_PIXELS))
    draw_button(screen, fonts, UNDO_BUTTON, "Undo")

    # Tour de jeu : une pastille de la couleur du joueur, puis le texte.
    x = BOARD_PIXELS + 30
    if result is None:
        center = (x + 12, 145)
        pygame.draw.circle(screen, stone_color(board.current_player), center, 12)
        pygame.draw.circle(screen, TEXT_COLOR, center, 12, 1)
        text = f"{player_name(board.current_player)} to play"
    else:
        text = "Game over"
    label = fonts["normal"].render(text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(midleft=(x + 32, 145)))

    # Pierres capturees par chaque joueur (10 = victoire).
    title = fonts["normal"].render("Captures", True, TEXT_COLOR)
    screen.blit(title, (x, 210))
    for i, player in enumerate((BLACK, WHITE)):
        line = f"{player_name(player)}: {board.captures[player]} / {CAPTURES_TO_WIN}"
        label = fonts["small"].render(line, True, TEXT_COLOR)
        screen.blit(label, (x, 245 + 30 * i))


def make_overlay():
    overlay = pygame.Surface((BOARD_PIXELS, BOARD_PIXELS), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    return overlay


def draw_popup(screen, fonts, overlay, result):
    """Popup au milieu du plateau quand la partie est finie."""
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, POPUP_COLOR, POPUP_RECT, border_radius=12)
    pygame.draw.rect(screen, LINE_COLOR, POPUP_RECT, 2, border_radius=12)
    title = "Draw" if result == DRAW else f"{player_name(result)} wins"
    label = fonts["big"].render(title, True, POPUP_TEXT_COLOR)
    screen.blit(label, label.get_rect(center=(POPUP_RECT.centerx,
                                             POPUP_RECT.top + 60)))
    draw_button(screen, fonts, POPUP_UNDO, "Undo")
    draw_button(screen, fonts, POPUP_RESTART, "Restart")


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Gomoku")
    fonts = {
        "big": pygame.font.Font(None, 64),
        "normal": pygame.font.Font(None, 30),
        "small": pygame.font.Font(None, 26),
    }
    ghosts = {BLACK: make_ghost(BLACK_STONE_COLOR),
              WHITE: make_ghost(WHITE_STONE_COLOR)}
    red_ghost = make_ghost(RED)
    overlay = make_overlay()
    clock = pygame.time.Clock()
    board = Board()
    result = None
    forbidden = compute_forbidden(board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                changed = False
                undo_clicked = (UNDO_BUTTON.collidepoint(event.pos)
                                or (result is not None
                                    and POPUP_UNDO.collidepoint(event.pos)))
                if undo_clicked:
                    if board.history:
                        board.undo()
                        changed = True
                elif result is not None and POPUP_RESTART.collidepoint(
                        event.pos):
                    board = Board()
                    changed = True
                elif result is None:
                    cell = pixel_to_intersection(*event.pos)
                    # La GUI verifie la legalite avant d'appeler play.
                    if cell is not None and board.is_legal(*cell):
                        board.play(*cell)
                        changed = True
                if changed:
                    result = compute_result(board)
                    forbidden = [] if result else compute_forbidden(board)

        draw_board(screen, board, forbidden)
        if result is None:
            hovered = pixel_to_intersection(*pygame.mouse.get_pos())
            if hovered is not None and board.get(*hovered) == EMPTY:
                if hovered in forbidden:
                    draw_ghost(screen, red_ghost, *hovered)
                else:
                    draw_ghost(screen, ghosts[board.current_player], *hovered)
        draw_panel(screen, fonts, board, result)
        if result is not None:
            draw_popup(screen, fonts, overlay, result)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
