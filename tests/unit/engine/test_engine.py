import unittest
import pytest
import time

from parameterized import parameterized
from chess_insights.engine.move_generators import generate_all_moves
from chess_insights.engine.engine import Engine

class TestEngine(unittest.TestCase):
    @pytest.fixture
    def engine(self):
        """Create an instance of the Engine with a fresh board."""
        return Engine()


    def test_engine_move(self):
        """Test if the engine selects a valid move."""
        # Generate all possible moves from the current board state
        engine = Engine()
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
    @parameterized.expand([(1,20), (2,400), (3, 8902), (4, 197281)])
    def test_engine_perft(self, depth, expected):
        engine = Engine()
        start_board_state = engine.board_state
        run_time = time.time()
        positions = engine.perft(depth, start_board_state)
        run_time = time.time() - run_time
        print(f"\nRan perft with depth = {depth}. Found: {positions} in {run_time} seconds")
        assert positions == expected, f"Engine perft for depth = {depth} should return {expected}"
