import unittest
from parameterized import parameterized
from chess_insights.chess_pieces.chess_piece import ChessPiece
from chess_insights.chess_pieces.chess_piece import ChessBoard


class TestChessPieceParentClass(unittest.TestCase):
    pass
#    def setUp(self):
#        self.chess_board = ChessBoard()
#        self.chess_piece = ChessPiece(self.chess_board)
#
#    def test_is_piece_in_path(self):
#        origin_square = 18
#
#        assert self.chess_piece.is_piece_in_path(origin_square, target_square)
#