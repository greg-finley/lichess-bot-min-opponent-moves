import chess
from chess.engine import PlayResult
from typing import Any, Dict
import random


class ExampleEngine:
    pass


class TiredPieces(ExampleEngine):
    def __init__(self):
        # Dict mapping square to move count
        self.piece_moves: Dict[chess.Square, int] = {}

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Move pieces in order of least moved first - pieces get tired!"""
        # Get all legal moves
        legal_moves = list(board.legal_moves)

        # Find moves with minimum tiredness
        min_moves = []
        min_tiredness = 9999

        for move in legal_moves:
            from_square = move.from_square

            # Get move count for this square (0 if never moved)
            move_count = self.piece_moves.get(from_square, 0)

            # Update min_moves list
            if move_count < min_tiredness:
                min_moves = [move]
                min_tiredness = move_count
            elif move_count == min_tiredness:
                min_moves.append(move)

        # Pick a random move from the least tired pieces
        chosen_move = random.choice(min_moves) if min_moves else None
        if not chosen_move:
            return PlayResult(resigned=True)

        # Update piece_moves dict
        from_square = chosen_move.from_square
        to_square = chosen_move.to_square

        # Remove the old position if it exists
        if from_square in self.piece_moves:
            del self.piece_moves[from_square]

        # Add the new position with incremented count
        self.piece_moves[to_square] = min_tiredness + 1

        return PlayResult(chosen_move, None)
