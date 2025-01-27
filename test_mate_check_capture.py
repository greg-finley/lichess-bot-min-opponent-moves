import chess
import chess.variant
import pytest
from mate_check_capture import MateCheckCapture


@pytest.fixture(autouse=True)
def engine():
    return MateCheckCapture()


@pytest.mark.parametrize("execution_number", range(100))
def test_prefers_mate_over_check(execution_number, engine):
    """Should choose checkmate even when check is available"""
    board = chess.Board("4k3/2R5/4K3/8/8/8/8/8 w - - 0 1")
    move = engine.search(board).move
    assert move.uci() == "c7c8"
    board.push(move)
    assert board.is_checkmate()


@pytest.mark.parametrize("execution_number", range(100))
def test_prefers_check_over_capture(execution_number, engine):
    """Should choose check even when capture is available"""
    board = chess.Board("4k3/4r3/8/8/5r2/4P3/r7/Qn2K3 w - - 0 1")
    move = engine.search(board).move
    assert move.uci() == "a1h8"
    board.push(move)
    assert board.is_check()


@pytest.mark.parametrize("execution_number", range(100))
def test_prefers_capture_over_advance(execution_number, engine):
    """Should choose capture even when advance is available"""
    board = chess.Board("1b2k3/1P2r3/5b1N/8/5r2/1N2N3/P7/QN2K3 w - - 0 1")
    move = engine.search(board).move
    assert move.uci() == "a1f6"
    board.push(move)
    assert board.is_capture(move)


@pytest.mark.parametrize("execution_number", range(100))
def test_advances_white(execution_number, engine):
    """Should advance up the board as white"""
    board = chess.Board("8/3k4/8/6r1/6P1/6PP/6PP/7K w - - 0 1")
    move = engine.search(board).move
    assert move.uci() == "h3h4"


@pytest.mark.parametrize("execution_number", range(100))
def test_advances_black(execution_number, engine):
    """Should advance down the board as black"""
    board = chess.Board("8/k7/pp6/1p6/1N4P1/6PP/6PP/7K b - - 0 1")
    move = engine.search(board).move
    assert move.uci() == "a6a5"


@pytest.mark.parametrize("execution_number", range(100))
def test_play_random(execution_number, engine):
    """Should do something if no advances or other options"""
    board = chess.Board("KR6/BR6/8/8/8/8/1ppppppp/bkbbbbbb b - - 0 1")
    move = engine.search(board).move
    assert move.uci() == "b1a2"


@pytest.mark.parametrize("execution_number", range(100))
def test_variant_checkmate(execution_number, engine):
    """Should play a winning move in a variant game"""
    board = chess.variant.KingOfTheHillBoard("7k/5B2/5PP1/3NPN2/3Q1N2/3QK3/8/8 w - - 0 1")
    move = engine.search(board).move
    assert move.uci() == "e3e4"
    board.push(move)
    assert board.is_variant_loss()


@pytest.mark.parametrize("execution_number", range(100))
def test_crazyhouse_placement(execution_number, engine):
    """Should play a valid move in crazyhouse if a drop is available"""
    board = chess.variant.CrazyhouseBoard("r1bq1bnr/2pppkpp/ppn5/8/8/3BP3/PPPP1PPP/RNBQK2R/Pn b KQ - 1 5")
    move = engine.search(board).move
    assert move.uci() == "N@f3"
