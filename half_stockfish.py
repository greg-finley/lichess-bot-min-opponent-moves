import chess
import chess.engine
import sys
from lib.config import Configuration
from lib import model
from lib.engine_wrapper import MinimalEngine
from chess.engine import PlayResult
from typing import Any, Optional, Union
import random

OPTIONS_TYPE = dict[str, Any]
COMMANDS_TYPE = list[str]
MOVE = Union[chess.engine.PlayResult, list[chess.Move]]

platform = sys.platform
file_extension = ".exe" if platform == "win32" else ""


class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""

    pass


class HalfStockfish(ExampleEngine):
    def __init__(
        self,
        commands: COMMANDS_TYPE,
        options: OPTIONS_TYPE,
        stderr: Optional[int],
        draw_or_resign: Configuration,
        game: Optional[model.Game],
        **popen_args: str,
    ):
        """Start Stockfish."""
        super().__init__(commands, options, stderr, draw_or_resign, game, **popen_args)
        self.engine = chess.engine.SimpleEngine.popen_uci(f"./TEMP/sf{file_extension}")

    def search(
        self,
        board: chess.Board,
        time_limit: chess.engine.Limit,
        ponder: bool,
        draw_offered: bool,
        root_moves: MOVE,
    ) -> chess.engine.PlayResult:
        if board.fullmove_number == 1 or random.random() < 0.5:
            return PlayResult(random.choice(list(board.legal_moves)), None)
        return self.engine.play(board, time_limit)
