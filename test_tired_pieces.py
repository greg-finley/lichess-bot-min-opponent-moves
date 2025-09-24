import chess
import pytest
from tired_pieces import TiredPieces


@pytest.fixture(autouse=True)
def engine():
    return TiredPieces()


def test_piece_moves_tracking(engine):
    """Should track moved pieces in piece_moves dict"""
    # Start with standard position
    board = chess.Board()

    # Initially piece_moves should be empty
    assert len(engine.piece_moves) == 0

    # Make a move
    move = engine.search(board).move

    # After move, piece_moves should have exactly one entry
    assert len(engine.piece_moves) == 1

    # The entry should map the destination square to a count of 1
    assert move.to_square in engine.piece_moves
    assert engine.piece_moves[move.to_square] == 1
