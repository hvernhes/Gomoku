import time
from dataclasses import dataclass
from src.ai.minimax import best_move
from src.game.Board import Board
from src.helpers.computation import (
    compute_forbidden,
    compute_result
)
from src.helpers.game_log import (
    new_log_path,
    save_game_log
)
from src.helpers.initialisation import iniatilze_game


@dataclass
class GameState:
    board: Board
    result: str | int | None
    forbidden: list[tuple[int, int]]
    ai_times: list[float]   # duree de reflexion de l'IA a chaque coup (s)
    log_path: str
    ai_player: int | None   # couleur de l'IA, None en hotseat

    @classmethod
    def new(
            cls,
            ai_player: int | None
    ) -> "GameState":

        board, result, forbidden = iniatilze_game()

        return cls(board, result, forbidden, [], new_log_path(), ai_player)

    def is_ai_turn(
            self
    ) -> bool:
        """C'est a l'IA de jouer : partie en cours et main a la couleur de
        l'IA (jamais en hotseat, ai_player vaut alors None)."""

        return (
            self.ai_player is not None
            and self.result is None
            and self.board.current_player == self.ai_player
        )

    def undo_for_human(
            self
    ) -> None:
        """Annule le dernier coup ; si la main revient a l'IA, annule aussi
        son coup, pour que ce soit a l'humain de jouer (sinon l'IA rejouerait
        aussitot la meme chose)."""

        self.board.undo()
        if (
            self.ai_player is not None
            and self.board.current_player == self.ai_player
            and self.board.history
        ):
            self.board.undo()

    def save_log(
            self
    ) -> None:

        save_game_log(
            self.log_path,
            self.board,
            self.ai_player,
            self.ai_times
        )

    def restart(
            self
    ) -> None:
        """La partie finie est sauvegardee avant d'etre remplacee."""

        self.save_log()
        self.board = Board()
        self.ai_times = []
        self.log_path = new_log_path()

    def refresh(
            self
    ) -> None:
        """Recalcule le resultat et les cases interdites apres un
        changement."""

        self.result = compute_result(self.board)
        # Cases interdites : inutile de les calculer pour l'IA.
        if self.result is not None or self.is_ai_turn():
            self.forbidden = []
        else:
            self.forbidden = compute_forbidden(self.board)

    def play_ai_turn(
            self
    ) -> None:

        start = time.perf_counter()
        cell = best_move(self.board)
        self.ai_times.append(time.perf_counter() - start)
        if cell is None:
            # Aucun coup legal alors que la partie n'est pas finie :
            # on la termine plutot que de reboucler.
            self.result = "draw"
        else:
            self.board.play(cell)
            self.result = compute_result(self.board)
        self.forbidden = (
            []
            if self.result is not None
            else compute_forbidden(self.board)
        )
