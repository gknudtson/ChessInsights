import unittest
from parameterized import parameterized
from chess_insights.chess_board import ChessBoard
from chess_insights.chess_pieces.white_pawn import WhitePawn
from chess_insights.chess_pieces.black_pawn import BlackPawn


class TestBlackPawn(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()
        self.chess_board.change_turn()
        self.black_pawn = BlackPawn(self.chess_board)
        self.white_pawn = WhitePawn(self.chess_board)

    def test_cant_move_when_not_turn(self):
        origin_square = 10
        target_square = origin_square - 8
        self.chess_board.change_turn()
        self.chess_board.add_black_pawn(origin_square)
        self.black_pawn.movement_manager(origin_square, target_square)
        assert not self.chess_board.is_square_occupied(target_square)

    def test_black_pawn_movement_invalid_no_piece_on_square(self):
        origin_square = 10
        target_square = origin_square - 8
        self.black_pawn.movement_manager(origin_square, target_square)
        assert not self.chess_board.is_square_occupied(target_square)

    @parameterized.expand([29, 36, 38, 44, 46, 52, 53, 54])
    def test_black_pawn_movement_invalid_target_square(self, target_square):
        origin_square = 45
        self.chess_board.add_black_pawn(origin_square)
        self.black_pawn.movement_manager(origin_square, target_square)
        assert not self.chess_board.is_square_occupied(target_square)

    def test_black_pawn_movement_off_board(self):
        origin_square = 0
        target_square = origin_square - 8
        self.chess_board.add_black_pawn(origin_square)
        self.black_pawn.movement_manager(origin_square, target_square)
        assert not self.chess_board.is_whites_turn()

    def test_black_pawn_movement_invalid_black_piece_in_the_way(self):
        origin_square = 10
        target_square = origin_square - 8
        self.chess_board.add_black_pawn(origin_square)
        self.chess_board.add_black_pawn(target_square)
        black_pawns = self.chess_board.get_black_pawns()
        self.black_pawn.movement_manager(origin_square, target_square)
        assert black_pawns == self.chess_board.get_black_pawns()

    def test_black_pawn_movement_invalid_white_piece_in_the_way(self):
        origin_square = 10
        target_square = origin_square - 8
        self.chess_board.add_black_pawn(origin_square)
        self.chess_board.add_white_pawn(target_square)
        black_pawns = self.chess_board.get_black_pawns()
        self.black_pawn.movement_manager(origin_square, target_square)
        assert black_pawns == self.chess_board.get_black_pawns()

    def test_black_pawn_movement_valid_forward(self):
        origin_square = 10
        target_square = origin_square - 8
        self.chess_board.add_black_pawn(origin_square)
        self.black_pawn.movement_manager(origin_square, target_square)
        assert self.chess_board.is_square_occupied(target_square)

    def test_black_pawn_movement_valid_double_push(self):
        origin_square = 50
        target_square = origin_square - 16
        self.chess_board.add_black_pawn(origin_square)
        self.black_pawn.movement_manager(origin_square, target_square)
        assert self.chess_board.is_square_occupied(target_square)

    def test_black_pawn_movement_non_starting_rank_double_push(self):
        origin_square = 40
        target_square = origin_square - 16
        self.chess_board.add_black_pawn(origin_square)
        self.black_pawn.movement_manager(origin_square, target_square)
        assert not self.chess_board.is_square_occupied(target_square)

    def test_black_pawn_movement_double_push_piece_in_way(self):
        origin_square = 50
        target_square = origin_square - 16
        self.chess_board.add_black_pawn(origin_square)
        self.chess_board.add_black_pawn(origin_square - 8)
        self.black_pawn.movement_manager(origin_square, target_square)
        assert not self.chess_board.is_square_occupied(target_square)

    def test_black_pawn_capture_white_piece(self):
        origin_square = 10
        target_square = origin_square - 9
        self.chess_board.add_black_pawn(origin_square)
        self.chess_board.add_white_pawn(target_square)
        self.black_pawn.movement_manager(origin_square, target_square)
        assert self.chess_board.is_black_piece_on_square(target_square)
        assert not self.chess_board.is_white_piece_on_square(target_square)

    def test_black_pawn_en_passant_capture(self):
        origin_square = 33
        target_square = 18
        self.chess_board.add_black_pawn(origin_square)
        self.chess_board.add_white_pawn(10)
        self.black_pawn.movement_manager(origin_square, origin_square - 8)
        self.white_pawn.movement_manager(10, 26)
        self.black_pawn.movement_manager(origin_square - 8, target_square)
        assert not self.chess_board.is_white_piece_on_square(26)
        assert self.chess_board.is_black_piece_on_square(target_square)

    def test_black_pawn_invalid_en_passant_capture(self):
        origin_square = 50
        target_square = 43
        self.chess_board.add_black_pawn(origin_square)
        self.chess_board.add_white_pawn(11)
        self.chess_board.add_white_pawn(15)
        self.black_pawn.movement_manager(origin_square, origin_square - 16)
        self.white_pawn.movement_manager(11, 27)
        self.black_pawn.movement_manager(origin_square - 16, origin_square - 24)
        self.white_pawn.movement_manager(15, 23)
        self.black_pawn.movement_manager(origin_square - 24, target_square)
        assert self.chess_board.is_white_piece_on_square(27)
        assert not self.chess_board.is_black_piece_on_square(target_square)
