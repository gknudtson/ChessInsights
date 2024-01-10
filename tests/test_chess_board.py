import unittest
from chess_insights.chess_board import ChessBoard


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.white_pawns = self.chess_board.get_white_pawns()
        self.black_pawns = self.chess_board.get_black_pawns()

    def test_change_turn(self):
        assert not self.chess_board.change_turn()

    def test_get_white_pawns_returns_int(self):
        self.assertIsInstance(self.chess_board.get_white_pawns(), int)

    def test_get_black_pawns_returns_int(self):
        self.assertIsInstance(self.chess_board.get_black_pawns(), int)

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

    def test_add_black_pawn(self):
        initial_black_pawns = self.black_pawns
        square = 10
        expected_result = initial_black_pawns | 2 ** square
        self.chess_board.add_black_pawn(square)
        updated_black_pawns = self.chess_board.get_black_pawns()
        self.assertEqual(updated_black_pawns, expected_result)

    def test_remove_black_pawn(self):
        initial_black_pawns = self.black_pawns
        square = 10
        expected_result = initial_black_pawns & ~(2 ** square)
        self.chess_board.remove_black_pawn(square)
        updated_black_pawns = self.chess_board.get_black_pawns()
        self.assertEqual(updated_black_pawns, expected_result)

    def test_square_occupied(self):
        square = 10
        assert not self.chess_board.is_square_occupied(square)
        self.chess_board.add_white_pawn(square)
        assert self.chess_board.is_square_occupied(square)

    def test_is_white_piece_on_square(self):
        square = 10
        assert not self.chess_board.is_white_piece_on_square(square)
        self.chess_board.add_white_pawn(square)
        assert self.chess_board.is_white_piece_on_square(square)

    def test_is_black_piece_on_square(self):
        square = 10
        assert not self.chess_board.is_black_piece_on_square(square)
        self.chess_board.add_black_pawn(square)
        assert self.chess_board.is_black_piece_on_square(square)

    def test_remove_piece_from_square(self):
        square = 10
        self.chess_board.add_black_pawn(square)
        self.chess_board.remove_black_piece(square)
        assert not self.chess_board.is_square_occupied(square)
        self.chess_board.add_white_pawn(square)
        self.chess_board.remove_white_piece(square)
        assert not self.chess_board.is_square_occupied(square)
