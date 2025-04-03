from chess_insights.backend.core.util.fen import board_from_fen, fen_from_board
import unittest


class TestFenMethods(unittest.TestCase):

    def test_default_starting_position(self):
        # Standard chess starting position FEN
        default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # Generate the board state from the FEN
        board_state = board_from_fen(default_fen)

        # Convert the board state back to FEN
        generated_fen = fen_from_board(board_state)

        # Assert the FENs are identical
        self.assertEqual(default_fen, generated_fen)

    def test_custom_position(self):
        # A custom FEN representing a partially played game
        custom_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 1 1"

        # Generate the board state from the FEN
        board_state = board_from_fen(custom_fen)

        # Convert the board state back to FEN
        generated_fen = fen_from_board(board_state)

        # Assert the FENs are identical
        self.assertEqual(custom_fen, generated_fen)

    def test_no_castling_no_en_passant(self):
        # FEN with no castling rights and no en passant
        custom_fen = "8/8/8/8/8/8/8/8 w - - 0 1"

        # Generate the board state from the FEN
        board_state = board_from_fen(custom_fen)

        # Convert the board state back to FEN
        generated_fen = fen_from_board(board_state)

        # Assert the FENs are identical
        self.assertEqual(custom_fen, generated_fen)

    def test_invalid_fen(self):
        # Invalid FEN string
        invalid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 0"

        # Assert that an exception is raised for invalid FEN
        with self.assertRaises(ValueError):
            board_from_fen(invalid_fen)

    def test_en_passant_square(self):
        # Position with en passant square
        custom_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 1 1"

        # Generate the board state from the FEN
        board_state = board_from_fen(custom_fen)

        # Verify en passant square
        en_passant_square = board_state.en_passant_square.board
        self.assertEqual(en_passant_square, 1 << 20)  # 'e3' corresponds to square index 20

        # Convert the board state back to FEN
        generated_fen = fen_from_board(board_state)

        # Assert the FENs are identical
        self.assertEqual(custom_fen, generated_fen)


if __name__ == "__main__":
    unittest.main()
