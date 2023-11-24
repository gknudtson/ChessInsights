import unittest
from chess_insights.chess_board import *


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.chessboard = ChessBoard()
        self.white_pawns = self.chessboard.get_white_pawns()
        self.squares = [2,10,17,18,19,26,64]

    def test_get_white_pawns_returns_array(self):
        self.assertIsInstance(self.white_pawns, int)

    def test_add_white_pawn(self):
        initial_white_pawns = self.white_pawns
        square = 10
        expected_result = initial_white_pawns | 2 ** square
        self.chessboard.add_white_pawn(square)
        updated_white_pawns = self.chessboard.get_white_pawns()
        self.assertEqual(updated_white_pawns, expected_result)

    def test_remove_white_pawn(self):
        initial_white_pawns = self.white_pawns
        square = 10
        expected_result = initial_white_pawns & ~(2 ** square)
        self.chessboard.remove_white_pawn(square)
        updated_white_pawns = self.chessboard.get_white_pawns()
        self.assertEqual(updated_white_pawns, expected_result)

    def test_square_occupied(self):
        square = 10
        self.assertFalse(self.chessboard.is_square_occupied(square))
        self.chessboard.add_white_pawn(square)
        self.assertTrue(self.chessboard.is_square_occupied(square))

    def test_white_to_move_first(self):
        self.assertTrue(self.chessboard.turn)

    def test_white_cant_move_when_not_turn(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chessboard.turn = False
        self.chessboard.add_white_pawn(pawn_square)
        self.chessboard.white_pawn_movement(pawn_square, square_to_move)
        self.assertFalse(self.chessboard.is_square_occupied(square_to_move))

    def test_white_pawn_movement_invalid_no_pawn_on_square(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chessboard.white_pawn_movement(pawn_square, square_to_move)
        self.assertFalse(self.chessboard.is_square_occupied(square_to_move))

    def test_white_pawn_movement_invalid_square_to_move(self):
        pawn_square = 10
        square_to_move = pawn_square - 8
        self.chessboard.add_white_pawn(pawn_square)
        self.chessboard.white_pawn_movement(pawn_square, square_to_move)
        self.assertFalse(self.chessboard.is_square_occupied(square_to_move))

    def test_white_pawn_movement_valid_forward(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chessboard.add_white_pawn(pawn_square)
        self.chessboard.white_pawn_movement(pawn_square, square_to_move)
        self.assertTrue(self.chessboard.is_square_occupied(square_to_move))

    def test_white_pawn_movement_valid_two_forward(self):
        pawn_square = 10
        square_to_move = pawn_square + 16
        self.chessboard.add_white_pawn(pawn_square)
        self.chessboard.white_pawn_movement(pawn_square, square_to_move)
        self.assertTrue(self.chessboard.is_square_occupied(square_to_move))

    def test_white_pawn_movement_non_starting_rank_two_forward(self):
        pawn_square = 19
        square_to_move = pawn_square + 16
        self.chessboard.add_white_pawn(pawn_square)
        self.chessboard.white_pawn_movement(pawn_square, square_to_move)
        self.assertFalse(self.chessboard.is_square_occupied(square_to_move))

    def test_white_pawn_movement_two_forward_piece_in_way(self):
        pawn_square = 10
        square_to_move = pawn_square + 16
        self.chessboard.add_white_pawn(pawn_square)
        self.chessboard.add_white_pawn(pawn_square + 8)
        self.chessboard.white_pawn_movement(pawn_square, square_to_move)
        self.assertFalse(self.chessboard.is_square_occupied(square_to_move))