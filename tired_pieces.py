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

        # Categorize moves by how many times the piece has moved
        moves_by_tiredness = {}

        for move in legal_moves:
            from_square = move.from_square

            # Find move count for this square
            move_count = 0
            for square, count in self.piece_moves:
                if square == from_square:
                    move_count = count
                    break

            # Group moves by tiredness level
            if move_count not in moves_by_tiredness:
                moves_by_tiredness[move_count] = []
            moves_by_tiredness[move_count].append(move)

        # Find the least tired pieces (lowest move count)
        min_tiredness = min(moves_by_tiredness.keys())
        eligible_moves = moves_by_tiredness[min_tiredness]

        # Pick a random move from the least tired pieces
        chosen_move = random.choice(eligible_moves)

        # Update piece_moves list
        from_square = chosen_move.from_square
        to_square = chosen_move.to_square

        # Remove the old entry if it exists
        self.piece_moves = [(s, c) for s, c in self.piece_moves if s != from_square]

        # Find current count for this piece
        current_count = 0
        for move_count in moves_by_tiredness:
            if chosen_move in moves_by_tiredness[move_count]:
                current_count = move_count
                break

        # Add the new position with incremented count
        self.piece_moves.append((to_square, current_count + 1))

        return PlayResult(chosen_move, None)
