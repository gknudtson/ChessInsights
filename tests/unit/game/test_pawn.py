import unittest

from chess_insights.game.chess_board import ChessBoard
from chess_insights.util.enum_chess_piece_type import Color, ChessPieceType
from chess_insights.engine.bitboard import BitBoard
from chess_insights.game.pawn import pawn_promotion, pawn_movement, \
    is_pawn_starting_rank, handle_en_passant, handle_en_passant_capture


class TestPawn(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.new_piece_locations = {}

    def test_pawn_double_move_sets_en_passant(self):
        origin_square = 8  # e2 (index 8 in bitboard)
        target_square = 24  # e4 (index 24 in bitboard)
        piece_type = Color.WHITE.get_color_piece_by_type(ChessPieceType.PAWN)
        en_passant_square = handle_en_passant(origin_square, target_square, piece_type.color)
        self.assertEqual(en_passant_square, 1 << 16)  # e3 should be en passant target

    def test_pawn_promotion(self):
        target_square = 56
        color = Color.WHITE
        piece_locations = {
            color.get_color_piece_by_type(ChessPieceType.PAWN): BitBoard(1 << target_square),
            color.get_color_piece_by_type(ChessPieceType.QUEEN): BitBoard(0)
        }
        pawn_promotion(target_square, piece_locations, color)
        self.assertEqual(piece_locations[color.get_color_piece_by_type(ChessPieceType.PAWN)].board,
                         0)
        self.assertNotEqual(
            piece_locations[color.get_color_piece_by_type(ChessPieceType.QUEEN)].board, 0)

    def test_pawn_movement_white(self):
        square = 8  # e2
        move1, move2 = pawn_movement(Color.WHITE, square)
        self.assertEqual(move1, 16)  # e3
        self.assertEqual(move2, 24)  # e4

    def test_pawn_movement_black(self):
        square = 48  # e7
        move1, move2 = pawn_movement(Color.BLACK, square)
        self.assertEqual(move1, 40)  # e6
        self.assertEqual(move2, 32)  # e5

    def test_pawn_starting_rank(self):
        self.assertTrue(is_pawn_starting_rank(8, Color.WHITE))  # White's second rank
        self.assertFalse(is_pawn_starting_rank(24, Color.WHITE))  # Not on the second rank
        self.assertTrue(is_pawn_starting_rank(48, Color.BLACK))  # Black's seventh rank
        self.assertFalse(is_pawn_starting_rank(40, Color.BLACK))  # Not on the seventh rank



if __name__ == "__main__":
    unittest.main()
