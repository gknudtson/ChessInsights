import unittest
from chess_insights.chess_board import ChessBoard
from chess_insights.chess_pieces.white_pawn import WhitePawn
from chess_insights.chess_pieces.black_pawn import BlackPawn


# TODO cleanup test code and ensure logic coverage
class TestWhitePawn(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.white_pawn = WhitePawn(self.chess_board)
        self.white_pawns = self.chess_board.get_white_pawns()
        self.black_pawn = BlackPawn(self.chess_board)
        self.squares = [2, 10, 17, 18, 19, 26, 64]

    def test_cant_move_when_not_turn(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chess_board.change_turn()
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_invalid_no_pawn_on_square(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_invalid_square_to_move(self):
        pawn_square = 101
        square_to_move = pawn_square - 8
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_invalid_white_piece_in_the_way(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chess_board.add_white_pawn(pawn_square)
        self.chess_board.add_white_pawn(square_to_move)
        white_pawns = self.chess_board.get_white_pawns()
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertEqual(white_pawns, self.chess_board.get_white_pawns())

    def test_white_pawn_movement_invalid_black_piece_in_the_way(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chess_board.add_white_pawn(pawn_square)
        self.chess_board.add_black_pawn(square_to_move)
        white_pawns = self.chess_board.get_white_pawns()
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertEqual(white_pawns, self.chess_board.get_white_pawns())

    def test_white_pawn_movement_valid_forward(self):
        pawn_square = 10
        square_to_move = pawn_square + 8
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertTrue(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_valid_two_forward(self):
        pawn_square = 10
        square_to_move = pawn_square + 16
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertTrue(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_non_starting_rank_two_forward(self):
        pawn_square = 19
        square_to_move = pawn_square + 16
        self.chess_board.add_white_pawn(pawn_square)
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_movement_two_forward_piece_in_way(self):
        pawn_square = 10
        square_to_move = pawn_square + 16
        self.chess_board.add_white_pawn(pawn_square)
        self.chess_board.add_white_pawn(pawn_square + 8)
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertFalse(self.chess_board.is_square_occupied(square_to_move))

    def test_white_pawn_capture_black_piece(self):
        pawn_square = 10
        square_to_move = pawn_square + 9
        self.chess_board.add_white_pawn(pawn_square)
        self.chess_board.add_black_pawn(square_to_move)
        self.white_pawn.movement_manager(pawn_square, square_to_move)
        self.assertTrue(self.chess_board.is_white_piece_on_square(square_to_move))
        self.assertFalse(self.chess_board.is_black_piece_on_square(square_to_move))

    def test_white_pawn_en_passant_capture(self):
        pawn_square = 26
        square_to_move = 43
        self.chess_board.add_white_pawn(pawn_square)
        self.chess_board.add_black_pawn(51)
        self.white_pawn.movement_manager(pawn_square, pawn_square + 8)
        self.black_pawn.movement_manager(51, 35)
        self.white_pawn.movement_manager(pawn_square + 8, square_to_move)
        self.assertTrue(self.chess_board.is_white_piece_on_square(square_to_move))

    def test_white_pawn_invalid_en_passant_capture(self):
        pawn_square = 10
        square_to_move = 43
        self.chess_board.add_white_pawn(pawn_square)
        self.chess_board.add_black_pawn(51)
        self.chess_board.add_black_pawn(55)
        self.white_pawn.movement_manager(pawn_square, pawn_square + 16)
        self.black_pawn.movement_manager(51, 35)
        self.white_pawn.movement_manager(pawn_square + 16, pawn_square + 24)
        self.black_pawn.movement_manager(55, 47)
        self.white_pawn.movement_manager(pawn_square + 24, square_to_move)
        self.assertFalse(self.chess_board.is_white_piece_on_square(square_to_move))
