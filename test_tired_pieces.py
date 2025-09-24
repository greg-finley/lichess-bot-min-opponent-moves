import chess
import pytest
from tired_pieces import TiredPieces

# NOTE: This library treats castling as a king move, like moving from e1 to g1.


@pytest.fixture(autouse=True)
def engine():
    return TiredPieces()


@pytest.mark.parametrize("execution_number", range(10))
def test_piece_moves_tracking(execution_number, engine):
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


@pytest.mark.parametrize("execution_number", range(10))
def test_multiple_pieces_tracking(execution_number):
    """Should track multiple pieces as they move"""
    # Create separate engines for each side
    white_engine = TiredPieces()
    black_engine = TiredPieces()

    # Start with king and pawn each
    board = chess.Board("k7/3p4/8/8/8/8/6P1/K7 w - - 0 1")

    # Initially empty for white
    assert len(white_engine.piece_moves) == 0

    # White moves first piece (either king or pawn)
    move1 = white_engine.search(board).move
    board.push(move1)
    assert len(white_engine.piece_moves) == 1
    assert white_engine.piece_moves[move1.to_square] == 1

    # Black moves (using separate engine instance)
    move2 = black_engine.search(board).move
    board.push(move2)
    # White's tracking should be unchanged
    assert len(white_engine.piece_moves) == 1
    # Black's tracking should have one entry
    assert len(black_engine.piece_moves) == 1
    assert black_engine.piece_moves[move2.to_square] == 1

    # White's second move - should prefer the unmoved piece
    move3 = white_engine.search(board).move
    board.push(move3)

    # Should have moved the other piece (not the same one twice)
    assert move3.from_square != move1.to_square
    assert len(white_engine.piece_moves) == 2
    assert white_engine.piece_moves[move3.to_square] == 1
