"""Journal d'une partie, ecrit en une fois a partir de board.history.

Sert a etudier une partie apres coup. Une erreur d'ecriture est ignoree : le
jeu ne doit jamais planter a cause du journal.
"""
import os
from datetime import datetime

from board import (
    BLACK,
    WHITE
)
from src.game.Board import Board
from src.helpers.computation import compute_result
from src.helpers.utils import opponent_of

PLAYER_NAMES = {BLACK: "Black", WHITE: "White"}

# Dossier logs/ a la racine du depot (ignore par git).
LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    ))),
    "logs"
)


def new_log_path(
        directory: str = LOG_DIR
) -> str:
    """Chemin du fichier de la partie qui commence."""

    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    return os.path.join(directory, f"game_{stamp}.log")


def save_game_log(
        path: str,
        board: Board,
        ai_player: int | None,
        ai_times: list[float],
        depth: int | None = None
) -> None:
    """Ecrit la partie telle qu'elle est (le fichier est ecrase) : coups,
    captures, resultat s'il y en a un, plateau final, temps de l'IA.
    Ne fait rien si aucun coup n'a ete joue."""

    if not board.history:
        return

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as log_file:
            log_file.write(_format_game(board, ai_player, ai_times, depth))
    except OSError:
        pass


def _format_game(
        board: Board,
        ai_player: int | None,
        ai_times: list[float],
        depth: int | None
) -> str:

    if ai_player is None:
        mode = "hotseat"
    else:
        mode = f"human vs AI, AI plays {PLAYER_NAMES[ai_player]}"
        if depth is not None:
            mode += f", depth {depth}"

    lines = [
        f"Game log - saved {datetime.now():%Y-%m-%d %H:%M:%S}"
        f" - mode: {mode}",
        "Coordinates are (row, col), from 0 to 18.",
        ""
    ]

    # history ne garde pas le joueur de chaque coup, et une pierre capturee
    # n'est plus sur la grille : on remonte l'alternance depuis le dernier
    # joueur (celui qui n'a pas la main).
    total = len(board.history)
    last_mover = opponent_of(board.current_player)
    captured_by = {BLACK: 0, WHITE: 0}
    for number, (row, col, captured) in enumerate(board.history, start=1):
        if (total - number) % 2 == 0:
            player = last_mover
        else:
            player = opponent_of(last_mover)
        name = PLAYER_NAMES[player]
        line = f"{number:<4}{name:<7}({row}, {col})"
        if captured:
            captured_by[player] += len(captured)
            # Tri : l'ordre de board.history depend de la direction de la
            # capture, le journal doit etre lisible et previsible.
            pairs = " ".join(
                f"({cell.row}, {cell.column})"
                for cell in sorted(
                    captured,
                    key=lambda cell: (cell.row, cell.column)
                )
            )
            line += f"  captured {pairs}  [{name}: {captured_by[player]}]"
        lines.append(line)

    lines.append("")
    result = compute_result(board)
    if result is None:
        lines.append("Result: game not finished")
    elif result == "draw":
        lines.append("Result: Draw")
    else:
        lines.append(f"Result: {PLAYER_NAMES[result]} wins")
    lines.append(
        f"Captures: Black {board.captures[BLACK]},"
        f" White {board.captures[WHITE]}"
    )
    if ai_times:
        # Apres un Undo, la liste peut contenir le temps d'un coup annule.
        lines.append(
            "AI times (s): "
            + ", ".join(f"{t:.2f}" for t in ai_times)
            + f"  ({len(ai_times)} moves,"
            f" average {sum(ai_times) / len(ai_times):.2f},"
            f" max {max(ai_times):.2f})"
        )
    lines.append("")
    lines.append("Final board (X = Black, O = White):")
    lines.append(str(board))

    return "\n".join(lines) + "\n"
