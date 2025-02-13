import pytest
from chess_insights.engine.move_generators import generate_all_moves
from chess_insights.game.chess_board import ChessBoard
from chess_insights.engine.engine import Engine
from chess_insights.util.enum_square import Square


@pytest.fixture
def engine():
    """Create an instance of the Engine with a fresh board."""
    return Engine()


def test_engine_move(engine):
    """Test if the engine selects a valid move."""
    # Generate all possible moves from the current board state
    candidate_moves = generate_all_moves(engine.board_state)

    # Flatten the list of valid moves
    valid_moves = [(origin, target) for targets, _, origin in candidate_moves for target in
                   engine._validate_moves(targets, _, origin)]

    # Ensure that there are valid moves available
    assert len(valid_moves) > 0, "No valid moves were generated!"

    # Get a move from the engine
    selected_move = engine.generate_move()

    # Ensure the move is a tuple of (origin, target)
    assert isinstance(selected_move, tuple), f"Move should be a tuple, got {type(selected_move)}"
    assert len(selected_move) == 2, "Move should contain two elements (origin, target)"

    # Ensure the move is in the list of valid moves
    assert selected_move in valid_moves, f"Engine selected an invalid move: {selected_move}"
