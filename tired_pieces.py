import chess
from chess.engine import PlayResult
from typing import Any, List, Tuple
import random


class ExampleEngine:
    pass


class TiredPieces(ExampleEngine):
    def __init__(self):
        # List of tuples: (square, move_count)
        self.piece_moves: List[Tuple[chess.Square, int]] = []

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Move pieces in order of least moved first - pieces get tired!"""
        # Get all legal moves
        legal_moves = list(board.legal_moves)

        # Find moves with minimum tiredness
        min_moves = []
        min_tiredness = 9999

        for move in legal_moves:
            from_square = move.from_square

            # Find move count for this square
            move_count = 0
            for square, count in self.piece_moves:
                if square == from_square:
                    move_count = count
                    break

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

        # Update piece_moves list
        from_square = chosen_move.from_square
        to_square = chosen_move.to_square

        # Remove the old entry if it exists
        self.piece_moves = [(s, c) for s, c in self.piece_moves if s != from_square]

        # Add the new position with incremented count
        self.piece_moves.append((to_square, min_tiredness + 1))

        return PlayResult(chosen_move, None)
