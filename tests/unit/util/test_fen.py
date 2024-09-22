import unittest
from chess_insights.util.enum_chess_piece_type import ColorChessPiece
from chess_insights.util.fen import board_from_fen


class TestBoardFromFen(unittest.TestCase):

    def test_default_starting_position(self):
        # Standard chess starting position FEN
        default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # Expected bitboards for the starting positions
        expected_white_pieces = {
            ColorChessPiece.WHITE_PAWN: 0xFF00,
            ColorChessPiece.WHITE_ROOK: 0x81,
            ColorChessPiece.WHITE_KNIGHT: 0x42,
            ColorChessPiece.WHITE_BISHOP: 0x24,
            ColorChessPiece.WHITE_QUEEN: 0x8,
            ColorChessPiece.WHITE_KING: 0x10
        }

        expected_black_pieces = {
            ColorChessPiece.BLACK_PAWN: 0xFF000000000000,
            ColorChessPiece.BLACK_ROOK: 0x8100000000000000,
            ColorChessPiece.BLACK_KNIGHT: 0x4200000000000000,
            ColorChessPiece.BLACK_BISHOP: 0x2400000000000000,
            ColorChessPiece.BLACK_QUEEN: 0x800000000000000,
            ColorChessPiece.BLACK_KING: 0x1000000000000000
        }

        # Generate the board state from the default FEN
        board_state = board_from_fen(default_fen)

        # Verify general board state
        self.assertTrue(board_state.is_whites_turn)
        self.assertEqual(board_state.en_passant_square.board, 0)
        self.assertEqual(board_state.fifty_move_rule, 0)
        self.assertEqual(board_state.move_number, 1)
        self.assertEqual(board_state.castling_rights, 0b1111)

        # Verify piece locations
        for piece, expected_board in expected_white_pieces.items():
            self.assertEqual(board_state.piece_locations[piece].board, expected_board)

        for piece, expected_board in expected_black_pieces.items():
            self.assertEqual(board_state.piece_locations[piece].board, expected_board)


if __name__ == "__main__":
    unittest.main()
