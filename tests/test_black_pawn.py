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
        pawn_square = 10
        square_to_move = pawn_square - 8
        self.chess_board.change_turn()
        self.chess_board.add_black_pawn(pawn_square)
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert not self.chess_board.is_square_occupied(square_to_move)

    def test_black_pawn_movement_invalid_no_piece_on_square(self):
        pawn_square = 10
        square_to_move = pawn_square - 8
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert not self.chess_board.is_square_occupied(square_to_move)

    @parameterized.expand([29, 36, 38, 44, 46, 52, 53, 54])
    def test_black_pawn_movement_invalid_square_to_move(self, square_to_move):
        pawn_square = 45
        self.chess_board.add_black_pawn(pawn_square)
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert not self.chess_board.is_square_occupied(square_to_move)

    def test_black_pawn_movement_off_board(self):
        pawn_square = 0
        square_to_move = pawn_square - 8
        self.chess_board.add_black_pawn(pawn_square)
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert not self.chess_board.is_whites_turn()

    def test_black_pawn_movement_invalid_black_piece_in_the_way(self):
        pawn_square = 10
        square_to_move = pawn_square - 8
        self.chess_board.add_black_pawn(pawn_square)
        self.chess_board.add_black_pawn(square_to_move)
        black_pawns = self.chess_board.get_black_pawns()
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert black_pawns == self.chess_board.get_black_pawns()

    def test_black_pawn_movement_invalid_white_piece_in_the_way(self):
        pawn_square = 10
        square_to_move = pawn_square - 8
        self.chess_board.add_black_pawn(pawn_square)
        self.chess_board.add_white_pawn(square_to_move)
        black_pawns = self.chess_board.get_black_pawns()
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert black_pawns == self.chess_board.get_black_pawns()

    def test_black_pawn_movement_valid_forward(self):
        pawn_square = 10
        square_to_move = pawn_square - 8
        self.chess_board.add_black_pawn(pawn_square)
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert self.chess_board.is_square_occupied(square_to_move)

    def test_black_pawn_movement_valid_double_push(self):
        pawn_square = 50
        square_to_move = pawn_square - 16
        self.chess_board.add_black_pawn(pawn_square)
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert self.chess_board.is_square_occupied(square_to_move)

    def test_black_pawn_movement_non_starting_rank_double_push(self):
        pawn_square = 40
        square_to_move = pawn_square - 16
        self.chess_board.add_black_pawn(pawn_square)
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert not self.chess_board.is_square_occupied(square_to_move)

    def test_black_pawn_movement_double_push_piece_in_way(self):
        pawn_square = 50
        square_to_move = pawn_square - 16
        self.chess_board.add_black_pawn(pawn_square)
        self.chess_board.add_black_pawn(pawn_square - 8)
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert not self.chess_board.is_square_occupied(square_to_move)

    def test_black_pawn_capture_white_piece(self):
        pawn_square = 10
        square_to_move = pawn_square - 9
        self.chess_board.add_black_pawn(pawn_square)
        self.chess_board.add_white_pawn(square_to_move)
        self.black_pawn.movement_manager(pawn_square, square_to_move)
        assert self.chess_board.is_black_piece_on_square(square_to_move)
        assert not self.chess_board.is_white_piece_on_square(square_to_move)

    def test_black_pawn_en_passant_capture(self):
        pawn_square = 33
        square_to_move = 18
        self.chess_board.add_black_pawn(pawn_square)
        self.chess_board.add_white_pawn(10)
        self.black_pawn.movement_manager(pawn_square, pawn_square - 8)
        self.white_pawn.movement_manager(10, 26)
        self.black_pawn.movement_manager(pawn_square - 8, square_to_move)
        assert not self.chess_board.is_white_piece_on_square(26)
        assert self.chess_board.is_black_piece_on_square(square_to_move)

    def test_black_pawn_invalid_en_passant_capture(self):
        pawn_square = 50
        square_to_move = 43
        self.chess_board.add_black_pawn(pawn_square)
        self.chess_board.add_white_pawn(11)
        self.chess_board.add_white_pawn(15)
        self.black_pawn.movement_manager(pawn_square, pawn_square - 16)
        self.white_pawn.movement_manager(11, 27)
        self.black_pawn.movement_manager(pawn_square - 16, pawn_square - 24)
        self.white_pawn.movement_manager(15, 23)
        self.black_pawn.movement_manager(pawn_square - 24, square_to_move)
        assert self.chess_board.is_white_piece_on_square(27)
        assert not self.chess_board.is_black_piece_on_square(square_to_move)
