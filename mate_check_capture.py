import chess
from chess.engine import PlayResult
from typing import Any
import random


class ExampleEngine:
    pass


class MateCheckCapture(ExampleEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Simple priorities: Checkmate > Check > Capture > Advance > Random."""
        checkmating_moves = []
        checking_moves = []
        capturing_moves = []
        advancing_moves = []
        random_moves = []
        for move in board.legal_moves:
            if board.is_capture(move):
                capturing_moves.append(move)
            board.push(move)
            if board.is_checkmate() or board.is_variant_loss():
                checkmating_moves.append(move)
            elif board.is_check():
                checking_moves.append(move)
            else:
                move_uci = move.uci()
                if "@" not in move_uci:
                    is_going_upboard = int(move_uci[1]) > int(move_uci[3])
                    is_going_downboard = int(move_uci[1]) < int(move_uci[3])
                    if board.turn == chess.WHITE and is_going_upboard:
                        advancing_moves.append(move)
                    elif board.turn == chess.BLACK and is_going_downboard:
                        advancing_moves.append(move)
                    else:
                        random_moves.append(move)
                else:
                    random_moves.append(move)
            board.pop()
        if checkmating_moves:
            return PlayResult(random.choice(checkmating_moves), None)
        elif checking_moves:
            return PlayResult(random.choice(checking_moves), None)
        elif capturing_moves:
            return PlayResult(random.choice(capturing_moves), None)
        elif advancing_moves:
            return PlayResult(random.choice(advancing_moves), None)
        return PlayResult(random.choice(random_moves), None)
