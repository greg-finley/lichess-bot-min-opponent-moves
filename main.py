import chess
from chess.engine import PlayResult
from typing import Any
import random


class ExampleEngine:
    pass


class MinOpponentMoves(ExampleEngine):
    """Choose a move among those that minimize the opponent's legal responses, selected at random."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose a random move among those minimizing the opponent's legal moves."""
        min_moves = []
        min_count = 9999
        for move in board.legal_moves:
            board.push(move)
            count = sum(1 for _ in board.legal_moves)
            board.pop()
            if count < min_count:
                min_moves = [move]
                min_count = count
            elif count == min_count:
                min_moves.append(move)
        chosen_move = random.choice(min_moves) if min_moves else None
        return PlayResult(chosen_move, None)
