import unittest
from chess_insights.chess_board import ChessBoard
from chess_insights.chess_pieces.white_pawn import WhitePawn


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.white_pawn = WhitePawn(self.chess_board)
        self.white_pawns = self.chess_board.get_white_pawns()
        self.squares = [2, 10, 17, 18, 19, 26, 64]

    def test_cant_move_when_not_turn(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chess_board.change_turn()
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.move(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_invalid_no_pawn_on_square(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.white_pawn.move(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_invalid_square_to_move(self):
        pawn_square = 10
        square_to_move = pawn_square - 8
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.move(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_valid_forward(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.move(pawn_square, square_to_move)
        self.assertTrue(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_valid_two_forward(self):
        pawn_square = 10
        square_to_move = pawn_square + 16
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.move(pawn_square, square_to_move)
        self.assertTrue(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_non_starting_rank_two_forward(self):
        pawn_square = 19
        square_to_move = pawn_square + 16
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.move(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_two_forward_piece_in_way(self):
        pawn_square = 10
        square_to_move = pawn_square + 16
        self.chess_board.add_white_pawn(pawn_square)
        self.chess_board.add_white_pawn(pawn_square + 8)
        self.white_pawn.move(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))
