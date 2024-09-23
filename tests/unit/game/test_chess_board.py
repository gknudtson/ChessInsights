import unittest
from parameterized import parameterized
from chess_insights.game.chess_board import ChessBoard, ColorChessPiece
from chess_insights.engine.bitboard import BitBoard


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_is_whites_turn(self):
        self.assertIsInstance(self.chess_board.is_whites_turn(), bool)

    def test_get_piece_locations_returns_BitBoard(self):
        self.assertIsInstance(self.chess_board.get_piece_locations(ColorChessPiece.WHITE_PAWN),
                              BitBoard)

    def test_square_occupied(self):
        square = 10
        self.assertFalse(self.chess_board.is_square_occupied(square))
        self.chess_board.add_piece(ColorChessPiece.WHITE_PAWN, square)
        self.assertTrue(self.chess_board.is_square_occupied(square))

    def test_is_piece_on_square(self):
        square = 10
        self.assertFalse(self.chess_board.is_piece_on_square(ColorChessPiece.WHITE_PAWN, square))
        self.chess_board.add_piece(ColorChessPiece.WHITE_PAWN, square)
        self.assertTrue(self.chess_board.is_piece_on_square(ColorChessPiece.WHITE_PAWN, square))

    def test_remove_piece_by_square(self):
        square = 10
        self.chess_board.add_piece(ColorChessPiece.BLACK_PAWN, square)
        self.chess_board.remove_piece(ColorChessPiece.BLACK_PAWN, square)
        self.assertFalse(self.chess_board.is_square_occupied(square))

    def test_update_all_pieces(self):
        square = 10
        self.chess_board.add_piece(ColorChessPiece.BLACK_PAWN, square)
        self.chess_board.add_piece(ColorChessPiece.WHITE_PAWN, square + 2)
        self.chess_board.update_all_pieces()
        self.assertEqual(self.chess_board.get_piece_locations(ColorChessPiece.ALL_PIECES).board,
                         5120)

    def test_find_piece_on_square(self):
        square = 10
        piece_type = ColorChessPiece.BLACK_PAWN
        self.chess_board.add_piece(piece_type, square)
        self.assertEqual(self.chess_board.get_piece_on_square(square), piece_type)

    def test_get_castling_rights(self):
        self.assertEqual(self.chess_board.get_castling_rights(), 0b1111)

    def test_update_castling_rights(self):
        self.chess_board.update_castling_rights(0b1011)
        self.assertEqual(self.chess_board.get_castling_rights(), 0b1011)

    @parameterized.expand([[42], [2], [21], [16], [36], [32], [4], [0]])
    def test_is_piece_in_path_no_pieces(self, target_square):
        origin_square = 18
        self.chess_board.add_piece(ColorChessPiece.WHITE_PAWN, origin_square)
        self.assertFalse(self.chess_board.is_piece_in_path(origin_square, target_square))

    @parameterized.expand([[42], [2], [21], [16], [36], [32], [4], [0]])
    def test_is_piece_in_path_piece_in_path(self, target_square):
        origin_square = 18
        self.chess_board.add_piece(ColorChessPiece.WHITE_PAWN, target_square)
        self.assertTrue(self.chess_board.is_piece_in_path(origin_square, target_square))

    @parameterized.expand([
        (10, ColorChessPiece.WHITE_PAWN, 655360),
        (17, ColorChessPiece.BLACK_KNIGHT, 21609056261),
        (28, ColorChessPiece.WHITE_ROOK, 1157442769150545936),
    ])
    def test_get_moves(self, square, piece_type, expected_board):
        self.chess_board.add_piece(piece_type, square)
        moves = self.chess_board.get_moves(square)
        self.assertEqual(moves.board, expected_board)

    def test_get_moves_with_collision_knight(self):
        self.chess_board.setup()
        moves = self.chess_board.get_moves(1).board
        self.assertEqual(moves, 327680)

    def test_get_moves_with_collision_queen(self):
        self.chess_board.setup()
        moves = self.chess_board.get_moves(4).board
        self.assertEqual(moves, 0)
    def test_get_moves_with_collision_pawn(self):
        self.chess_board.setup()
        self.chess_board.add_piece(ColorChessPiece.WHITE_ROOK, 16)
        self.chess_board.add_piece(ColorChessPiece.BLACK_PAWN, 18)
        moves = self.chess_board.get_moves(9).board
        self.assertEqual(moves, 262144)

    @parameterized.expand([
        ('white', ColorChessPiece.WHITE_PAWN, 2 ** 10),
        ('black', ColorChessPiece.BLACK_PAWN, 2 ** 10),
    ])
    def test_get_pieces_by_color(self, color, piece_type, expected_board):
        self.chess_board.add_piece(piece_type, 10)
        color_pieces = self.chess_board.__get_pieces_by_color(color)
        self.assertEqual(color_pieces, expected_board)


if __name__ == "__main__":
    unittest.main()
