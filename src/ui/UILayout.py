from dataclasses import dataclass
import pygame


@dataclass
class UILayout:

    undo_panel_button: pygame.Rect
    popup_rectangle: pygame.Rect
    popup_undo_button: pygame.Rect
    popup_restart_button: pygame.Rect
