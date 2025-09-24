import chess
import chess.variant
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

    # Black's second move
    move4 = black_engine.search(board).move
    board.push(move4)

    # White's third move - both pieces have moved once, so should pick randomly
    move5 = white_engine.search(board).move
    board.push(move5)

    # Should still have 2 entries, one with count=2
    assert len(white_engine.piece_moves) == 2
    # One piece should have count=2, the other count=1
    counts = sorted(white_engine.piece_moves.values())
    assert counts == [1, 2]


@pytest.mark.parametrize("execution_number", range(10))
def test_crazyhouse_prioritizes_drops(execution_number):
    """Should always drop pieces in crazyhouse, regardless of piece tiredness"""
    engine = TiredPieces()

    # Crazyhouse position with pieces in pocket (two pawns for white)
    # Even if king/pawn are fresh, we should still drop
    board = chess.variant.CrazyhouseBoard("k7/3p4/8/8/8/8/6P1/K7[PP] w - - 0 1")

    # Make a move - should be a drop
    move = engine.search(board).move
    assert move.drop, "Should have dropped a piece from pocket"
    assert move.uci().startswith("P@"), "Should drop a pawn"

    # After drop, piece should have count 1
    assert len(engine.piece_moves) == 1
    assert engine.piece_moves[move.to_square] == 1


@pytest.mark.parametrize("execution_number", range(10))
def test_atomic_fresh_piece_wins(execution_number):
    """In atomic, should play the fresh knight even if it explodes, since it's checkmate"""
    engine = TiredPieces()

    # Atomic position - knight on a6 is fresh, other pieces are tired
    board = chess.variant.AtomicBoard("1Bk5/2p5/N7/2K5/1B6/8/8/8 w - - 0 1")

    # Manually set up tired pieces (king and bishops have moved, knight hasn't)
    engine.piece_moves[chess.C5] = 3  # King has moved 3 times
    engine.piece_moves[chess.B8] = 2  # Bishop has moved 2 times
    engine.piece_moves[chess.B4] = 2  # Bishop has moved 2 times
    # Knight on a6 is not in the dict, so it has 0 moves

    # Should play Nxc7 because knight is freshest
    move = engine.search(board).move
    assert move.uci() == "a6c7", f"Should play Nxc7 for mate, got {move.uci()}"

    # Verify it's actually mate (king exploded)
    board.push(move)
    assert board.is_variant_loss()
    assert board.is_game_over()
