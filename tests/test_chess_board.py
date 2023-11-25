import unittest
from chess_insights.chess_board import ChessBoard


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.white_pawns = self.chess_board.get_white_pawns()
        self.squares = [2, 10, 17, 18, 19, 26, 64]

    def test_change_turn(self):
        self.assertFalse(self.chess_board.change_turn())

    def test_get_white_pawns_returns_int(self):
        self.assertIsInstance(self.chess_board.get_white_pawns(), int)

    def test_add_white_pawn(self):
        initial_white_pawns = self.white_pawns
        square = 10
        expected_result = initial_white_pawns | 2 ** square
        self.chess_board.add_white_pawn(square)
        updated_white_pawns = self.chess_board.get_white_pawns()
        self.assertEqual(updated_white_pawns, expected_result)

    def test_remove_white_pawn(self):
        initial_white_pawns = self.white_pawns
        square = 10
        expected_result = initial_white_pawns & ~(2 ** square)
        self.chess_board.remove_white_pawn(square)
        updated_white_pawns = self.chess_board.get_white_pawns()
        self.assertEqual(updated_white_pawns, expected_result)

    def test_square_occupied(self):
        square = 10
        self.assertFalse(self.chess_board.is_square_occupied(square))
        self.chess_board.add_white_pawn(square)
        self.assertTrue(self.chess_board.is_square_occupied(square))
