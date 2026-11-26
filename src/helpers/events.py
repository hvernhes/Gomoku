import pygame
from src.game.Cell import Cell
from src.game.GameState import GameState
from src.helpers.computation import pixel_to_intersection
from src.ui.UILayout import UILayout


def handle_click(
        pos,
        state: GameState,
        layout: UILayout
) -> bool:

    changed = False

    if state.is_ai_turn():
        return changed

    if state.result is None:
        if layout.undo_panel_button.collidepoint(pos):
            if state.board.history:
                state.undo_for_human()
                changed = True

        cell = pixel_to_intersection(*pos)

        if cell is not None:
            cell = Cell(*cell)

            if state.board.is_legal(cell):
                state.board.play(cell)

                changed = True

    else:
        if layout.popup_undo_button.collidepoint(pos):
            if state.board.history:
                state.undo_for_human()
                changed = True
        elif layout.popup_restart_button.collidepoint(pos):
            state.restart()
            changed = True

    return changed


def process_events(
        state: GameState,
        layout: UILayout
) -> bool:
    """Lit les evenements. Renvoie False quand la fenetre est fermee."""

    running = True
    changed = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if handle_click(event.pos, state, layout):
                changed = True

    if changed:
        state.refresh()

    return running
