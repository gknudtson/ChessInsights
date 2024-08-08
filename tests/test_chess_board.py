import unittest
from parameterized import parameterized
from chess_insights.chess_board import ChessBoard


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_change_turn(self):
        self.chess_board.change_turn()
        self.assertFalse(self.chess_board.is_whites_turn())

    def test_get_white_pawns_returns_int(self):
        self.assertIsInstance(self.chess_board.get_piece_locations('white', 'pawn'), int)

    def test_get_black_pawns_returns_int(self):
        self.assertIsInstance(self.chess_board.get_piece_locations('black', 'pawn'), int)

    def test_add_white_pawn(self):
        initial_white_pawns = self.chess_board.get_piece_locations('white', 'pawn')
        square = 10
        expected_result = initial_white_pawns | (1 << square)
        self.chess_board.add_piece('white', 'pawn', square)
        updated_white_pawns = self.chess_board.get_piece_locations('white', 'pawn')
        self.assertEqual(updated_white_pawns, expected_result)

    def test_remove_white_pawn(self):
        self.chess_board.add_piece('white', 'pawn', 10)
        initial_white_pawns = self.chess_board.get_piece_locations('white', 'pawn')
        square = 10
        expected_result = initial_white_pawns & ~(1 << square)
        self.chess_board.remove_piece('white', 'pawn', square)
        updated_white_pawns = self.chess_board.get_piece_locations('white', 'pawn')
        self.assertEqual(updated_white_pawns, expected_result)

    def test_add_black_pawn(self):
        initial_black_pawns = self.chess_board.get_piece_locations('black', 'pawn')
        square = 10
        expected_result = initial_black_pawns | (1 << square)
        self.chess_board.add_piece('black', 'pawn', square)
        updated_black_pawns = self.chess_board.get_piece_locations('black', 'pawn')
        self.assertEqual(updated_black_pawns, expected_result)

    def test_remove_black_pawn(self):
        self.chess_board.add_piece('black', 'pawn', 10)
        initial_black_pawns = self.chess_board.get_piece_locations('black', 'pawn')
        square = 10
        expected_result = initial_black_pawns & ~(1 << square)
        self.chess_board.remove_piece('black', 'pawn', square)
        updated_black_pawns = self.chess_board.get_piece_locations('black', 'pawn')
        self.assertEqual(updated_black_pawns, expected_result)

    def test_square_occupied(self):
        square = 10
        self.assertFalse(self.chess_board.is_square_occupied(square))
        self.chess_board.add_piece('white', 'pawn', square)
        self.assertTrue(self.chess_board.is_square_occupied(square))

    def test_is_white_piece_on_square(self):
        square = 10
        self.assertFalse(self.chess_board.is_piece_on_square('white', 'pawn', square))
        self.chess_board.add_piece('white', 'pawn', square)
        self.assertTrue(self.chess_board.is_piece_on_square('white', 'pawn', square))

    def test_is_black_piece_on_square(self):
        square = 10
        self.assertFalse(self.chess_board.is_piece_on_square('black', 'pawn', square))
        self.chess_board.add_piece('black', 'pawn', square)
        self.assertTrue(self.chess_board.is_piece_on_square('black', 'pawn', square))

    def test_remove_piece_from_square(self):
        square = 10
        self.chess_board.add_piece('black', 'pawn', square)
        self.chess_board.remove_piece('black', 'pawn', square)
        self.assertFalse(self.chess_board.is_square_occupied(square))
        self.chess_board.add_piece('white', 'pawn', square)
        self.chess_board.remove_piece('white', 'pawn', square)
        self.assertFalse(self.chess_board.is_square_occupied(square))

    @parameterized.expand([[42], [2], [21], [16], [36], [32], [4], [0]])
    def test_is_piece_in_path_no_pieces(self, target_square):
        origin_square = 18
        self.chess_board.add_piece('white', 'pawn', origin_square)
        self.assertFalse(self.chess_board.is_piece_in_path(origin_square, target_square))

    @parameterized.expand([[42], [2], [21], [16], [36], [32], [4], [0]])
    def test_is_piece_in_path_piece_in_path(self, target_square):
        origin_square = 18
        self.chess_board.add_piece('white', 'pawn', target_square)
        self.assertTrue(self.chess_board.is_piece_in_path(origin_square, target_square))


if __name__ == "__main__":
    unittest.main()
