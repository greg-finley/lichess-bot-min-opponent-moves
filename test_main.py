import chess
import pytest
from main import MinOpponentMoves


@pytest.fixture(autouse=True)
def engine():
    return MinOpponentMoves()


def test_checkmate(engine):
    """Play a checkmate in one move"""
    board = chess.Board(
        "r1bqkbnr/p1pp1ppp/2n5/1p2p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1"
    )  # Fool's mate
    # Do a bunch of times to make sure it's consistent
    for _ in range(100):
        result = engine.search(board)
        assert result.move == chess.Move.from_uci("f3f7")


def test_either_move(engine):
    """King can capture either pawn and results in same number of moves for opponent"""
    board = chess.Board("k7/8/8/8/8/5pp1/6K1/8 w - - 0 1")
    took_left = False
    took_right = False
    for _ in range(100):
        result = engine.search(board)
        if result.move == chess.Move.from_uci("g2f3"):
            took_left = True
        elif result.move == chess.Move.from_uci("g2g3"):
            took_right = True
        else:
            assert False

    assert took_left and took_right
