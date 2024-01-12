import unittest
from parameterized import parameterized
from chess_insights.chess_board import ChessBoard
from chess_insights.chess_pieces.white_king import WhiteKing
from chess_insights.chess_pieces.black_pawn import BlackPawn


class TestWhiteKing(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.white_king = WhiteKing(self.chess_board)
        self.black_pawn = BlackPawn(self.chess_board)
        self.origin_square = 4
        self.chess_board.add_white_king(self.origin_square)

    def test_invalid_move_when_not_turn(self):
        target_square = self.origin_square + 8
        self.chess_board.change_turn()
        self.white_king.movement_manager(self.origin_square, target_square)
        assert not self.chess_board.is_white_king_on_square(target_square)

    def test_invalid_move_when_not_on_origin_square(self):
        target_square = self.origin_square + 8
        self.white_king.movement_manager(self.origin_square - 1, target_square)
        assert not self.chess_board.is_white_king_on_square(target_square)

    def test_invalid_move_off_board(self):
        target_square = self.origin_square - 8
        self.white_king.movement_manager(self.origin_square, target_square)
        assert self.chess_board.is_white_king_on_square(self.origin_square)

    @parameterized.expand([34, 35, 36, 37, 38, 30, 22, 14, 6, 5, 4, 3, 2, 10, 18, 26])
    def test_invalid_move_distance(self, target_square):
        origin_square = 20
        self.chess_board.add_white_king(origin_square)
        self.chess_board.remove_white_king(4)
        self.white_king.movement_manager(origin_square, target_square)
        assert not self.chess_board.is_white_king_on_square(target_square)

    @parameterized.expand([0, 1, 2, 8, 10, 16, 17, 18])
    def test_valid_movement(self, target_square):
        origin_square = 9
        self.chess_board.add_white_king(origin_square)
        self.white_king.movement_manager(origin_square, target_square)
        assert self.chess_board.is_white_king_on_square(target_square)

    def test_valid_capture(self):
        target_square = self.origin_square + 8
        self.chess_board.add_black_pawn(target_square)
        self.white_king.movement_manager(self.origin_square, target_square)
        assert not self.chess_board.is_black_piece_on_square(target_square)
        assert self.chess_board.is_white_king_on_square(target_square)
