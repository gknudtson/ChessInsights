import unittest
from parameterized import parameterized
from chess_insights.chess_board import ChessBoard
from chess_insights.chess_pieces.white_king import WhiteKing


class TestWhiteKing(unittest.TestCase): # TODO: add invalid castling after rook movement test after implementing rook & check for revealed checks
    def setUp(self):
        self.chess_board = ChessBoard()
        self.white_king = WhiteKing(self.chess_board)
        self.origin_square = 4
        self.chess_board.add_piece('white', 'king', self.origin_square)

    def test_invalid_move_when_not_turn(self):
        target_square = self.origin_square + 8
        self.chess_board.change_turn()
        self.white_king.move(self.origin_square, target_square)
        self.assertFalse(self.chess_board.is_piece_on_square('white', 'king', target_square))

    def test_invalid_move_when_not_on_origin_square(self):
        target_square = self.origin_square + 8
        self.white_king.move(self.origin_square - 1, target_square)
        self.assertFalse(self.chess_board.is_piece_on_square('white', 'king', target_square))

    def test_invalid_move_off_board(self):
        target_square = self.origin_square - 8
        self.white_king.move(self.origin_square, target_square)
        self.assertTrue(self.chess_board.is_piece_on_square('white', 'king', self.origin_square))

    @parameterized.expand([[2], [3], [4], [5], [6], [10], [14], [18], [22], [26], [30], [34], [35], [36], [37], [38], [60]])
    def test_invalid_move_distance(self, target_square):
        origin_square = 20
        self.chess_board.add_piece('white', 'king', origin_square)
        self.chess_board.remove_piece('white', 'king', self.origin_square)
        self.chess_board.update_castling_rights(0)
        self.white_king.move(origin_square, target_square)
        self.assertFalse(self.chess_board.is_piece_on_square('white', 'king', target_square))

    @parameterized.expand([[0], [1], [2], [8], [10], [16], [17], [18]])
    def test_valid_movement(self, target_square):
        origin_square = 9
        self.chess_board.add_piece('white', 'king', origin_square)
        self.white_king.move(origin_square, target_square)
        self.assertTrue(self.chess_board.is_piece_on_square('white', 'king', target_square))

    def test_valid_capture(self):
        target_square = self.origin_square + 8
        self.chess_board.add_piece('black', 'pawn', target_square)
        self.white_king.move(self.origin_square, target_square)
        self.assertFalse(self.chess_board.is_piece_on_square('black', 'pawn', target_square))
        self.assertTrue(self.chess_board.is_piece_on_square('white', 'king', target_square))

    @parameterized.expand([(2, 0), (6, 7)])
    def test_valid_castling(self, target_square, rook_square):
        self.chess_board.add_piece('white', 'rook', rook_square)
        self.white_king.move(self.origin_square, target_square)
        self.assertFalse(self.chess_board.is_piece_on_square('white', 'king', self.origin_square))
        self.assertFalse(self.chess_board.is_piece_on_square('white', 'rook', rook_square))

    def test_invalid_castling_after_king_movement(self):
        self.white_king.move(self.origin_square, 5)
        self.chess_board.change_turn()
        self.white_king.move(5, 4)
        self.chess_board.change_turn()
        self.white_king.move(self.origin_square, 6)
        self.white_king.move(self.origin_square, 2)
        self.assertTrue(self.chess_board.is_piece_on_square('white', 'king', self.origin_square))

#    @parameterized.expand([2, 6])
#    def test_invalid_castling_movement_through_attacked_square(self, target_square):
#        self.chess_board.add_piece('black', 'pawn', self.origin_square + 8)
#        self.white_king.move(self.origin_square, target_square)
#        self.assertTrue(self.chess_board.is_piece_on_square('white', 'king', self.origin_square))

    @parameterized.expand([(2, 3), (6, 5)])
    def test_invalid_castling_white_piece_in_path(self, target_square, white_piece_square):
        self.chess_board.add_piece('white', 'pawn', white_piece_square)
        self.white_king.move(self.origin_square, target_square)
        self.assertTrue(self.chess_board.is_piece_on_square('white', 'king', self.origin_square))

    @parameterized.expand([(2, 3), (6, 5)])
    def test_invalid_castling_black_piece_in_path(self, target_square, black_piece_square):
        self.chess_board.add_piece('black', 'bishop', black_piece_square)
        self.white_king.move(self.origin_square, target_square)
        self.assertTrue(self.chess_board.is_piece_on_square('white', 'king', self.origin_square))

#   @parameterized.expand([2, 6])
#   def test_invalid_castling_king_under_check(self, target_square):
#       self.chess_board.add_piece('black', 'rook', 60)
#       self.white_king.move(self.origin_square, target_square)
#       self.assertTrue(self.chess_board.is_piece_on_square('white', 'king', self.origin_square))

if __name__ == "__main__":
    unittest.main()
