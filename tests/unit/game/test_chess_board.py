import unittest
from dataclasses import replace

from parameterized import parameterized

from chess_insights.game.chess_board import ChessBoard
from chess_insights.util.enum_chess_piece_type import ColorChessPiece, ChessPieceType, Color
from chess_insights.engine.bitboard import BitBoard
from chess_insights.util.enum_game_status import GameStatus
from chess_insights.util.enum_square import Square


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        """Initialize a new ChessBoard before each test."""
        self.chess_board = ChessBoard()

    # Test Utility Functions (Moved out of ChessBoard class)
    def is_square_occupied(self, square: int) -> bool:
        return (self.chess_board.board_state.piece_locations[ColorChessPiece.ALL_PIECES].board &
                (1 << square)) != 0

    def is_piece_on_square(self, piece: ColorChessPiece, square: int) -> bool:
        piece_locations = self.chess_board.board_state.piece_locations.get(piece, BitBoard()).board
        return (piece_locations & (1 << square)) != 0

    def get_piece_locations(self, piece: ColorChessPiece) -> BitBoard:
        return self.chess_board.board_state.piece_locations.get(piece, None)

    def get_castling_rights(self) -> int:
        return self.chess_board.board_state.castling_rights

    def is_whites_turn(self) -> bool:
        return self.chess_board.board_state.is_whites_turn

    def test_is_whites_turn(self):
        """Ensure that the turn-tracking logic works correctly."""
        self.assertIsInstance(self.is_whites_turn(), bool)

    def test_get_piece_locations_returns_BitBoard(self):
        """Ensure get_piece_locations() returns a BitBoard object."""
        self.assertIsInstance(self.get_piece_locations(ColorChessPiece.WHITE_PAWN), BitBoard)

    def test_is_square_occupied(self):
        """Check if a square is properly detected as occupied."""
        self.assertFalse(self.is_square_occupied(Square.e4.value))
        self.assertTrue(self.is_square_occupied(Square.e2.value))

    def test_is_piece_on_square(self):
        """Verify if a specific piece is detected at a square."""
        square = Square.e4.value
        self.chess_board = ChessBoard(
            board_state=self.chess_board._generate_move_board_state(Square.e2.value, square))
        self.assertTrue(self.is_piece_on_square(ColorChessPiece.WHITE_PAWN, square))

    def test_find_piece_on_square(self):
        """Ensure `get_piece_on_square()` correctly identifies the piece type."""
        square = Square.c3.value
        new_board = ChessBoard(board_state=self.chess_board._generate_move_board_state(Square.c2.value, square))
        self.assertEqual(new_board.get_piece_on_square(square), ColorChessPiece.WHITE_PAWN)

    def test_get_castling_rights(self):
        """Ensure the castling rights are correct at game start."""
        self.assertEqual(self.get_castling_rights(), 0b1111)

    def test_castling_rights_update(self):
        """Ensure castling rights update when moving a rook."""
        board = ChessBoard("1k6/8/8/8/8/8/8/R3K2R w KQ - 0 1")
        new_board = ChessBoard(
            board_state=board._generate_move_board_state(Square.h1.value, Square.h2.value))  # Move white rook
        self.assertEqual(new_board.board_state.castling_rights, 0b0010)

    @parameterized.expand([
        (Square.e2.value, [Square.e3.value, Square.e4.value]),  # Pawn move
        (Square.g1.value, [Square.f3.value, Square.h3.value]),  # Knight move
    ])
    def test_get_moves(self, square, expected_moves):
        """Check move generation for different pieces."""
        moves = self.chess_board.get_moves(square)
        self.assertEqual(set(moves), set(expected_moves))

    def test_get_moves_with_collision(self):
        """Ensure move generation respects collisions with other pieces."""
        expected_moves = [Square.d2.value, Square.d3.value]
        board = ChessBoard("rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2")
        moves = board.get_moves(Square.d1.value)  # Queen
        self.assertNotIn(set(expected_moves), set(moves))

    def test_pawn_capture(self):
        """Ensure pawns can capture diagonally but not move sideways."""
        board = ChessBoard("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
        self.chess_board = ChessBoard(
            board_state=board._generate_move_board_state(Square.e4.value, Square.d5.value))
        self.assertTrue(self.is_piece_on_square(ColorChessPiece.WHITE_PAWN, Square.d5.value))
        self.assertFalse(self.is_piece_on_square(ColorChessPiece.BLACK_PAWN, Square.d5.value))

    def test_en_passant(self):
        """Test en passant capture logic."""
        board = ChessBoard("rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3")
        self.chess_board = ChessBoard(
            board_state=board._generate_move_board_state(Square.e5.value, Square.f6.value))
        self.assertTrue(self.is_piece_on_square(ColorChessPiece.WHITE_PAWN, Square.f6.value))
        self.assertFalse(self.is_piece_on_square(ColorChessPiece.BLACK_PAWN, Square.f5.value))

    def test_castling_kingside(self):
        """Ensure kingside castling works correctly."""
        self.chess_board = ChessBoard("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
        new_board = ChessBoard(
            board_state=self.chess_board._generate_move_board_state(Square.e1.value, Square.g1.value))
        self.assertEqual(new_board.get_piece_on_square(Square.g1.value), ColorChessPiece.WHITE_KING)
        self.assertEqual(new_board.get_piece_on_square(Square.f1.value), ColorChessPiece.WHITE_ROOK)

    def test_castling_queenside(self):
        """Ensure queenside castling works correctly."""
        self.chess_board = ChessBoard("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
        new_board = ChessBoard(
            board_state=self.chess_board._generate_move_board_state(Square.e1.value, Square.c1.value))
        self.assertEqual(new_board.get_piece_on_square(Square.c1.value), ColorChessPiece.WHITE_KING)
        self.assertEqual(new_board.get_piece_on_square(Square.d1.value), ColorChessPiece.WHITE_ROOK)

    def test_get_moves_empty_square(self):
        """Ensure no moves are returned for an empty square."""
        moves = self.chess_board.get_moves(Square.e4.value)
        self.assertEqual(moves, [])

    def test_check_detection(self):
        """Ensure the game recognizes check."""
        self.chess_board = ChessBoard("r3k2r/8/8/8/8/4Q3/8/R3K2R b KQkq - 0 1")
        expected_moves = [61, 59, 51, 53]
        king_moves = self.chess_board.get_moves(Square.e8.value)
        self.assertEqual(set(king_moves), set(expected_moves))

    def test_checkmate_detection(self):
        """Ensure checkmate is correctly detected."""
        self.chess_board = ChessBoard(
            "r1bk1Qnr/p1pp2pp/np6/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQ - 0 4")
        king_moves = self.chess_board.get_moves(Square.e8.value)
        self.assertEqual(set(king_moves), set())  # King should be checkmated

    def test_check_get_game_status(self):
        """Ensure checkmate is correctly detected."""
        self.chess_board = ChessBoard(
            "rnbqkb1r/ppp2Qpp/3p1n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
        status = self.chess_board.check_game_status(self.chess_board.board_state)
        self.assertEqual(status, GameStatus.CHECKMATE)

    def test_initial_board_setup(self):
        """Ensure that all pieces are correctly positioned at game start."""
        expected_positions = {
            Square.a1.value: ColorChessPiece.WHITE_ROOK,
            Square.b1.value: ColorChessPiece.WHITE_KNIGHT,
            Square.c1.value: ColorChessPiece.WHITE_BISHOP,
            Square.d1.value: ColorChessPiece.WHITE_QUEEN,
            Square.e1.value: ColorChessPiece.WHITE_KING,
            Square.f1.value: ColorChessPiece.WHITE_BISHOP,
            Square.g1.value: ColorChessPiece.WHITE_KNIGHT,
            Square.h1.value: ColorChessPiece.WHITE_ROOK,
            Square.a2.value: ColorChessPiece.WHITE_PAWN,
            Square.h2.value: ColorChessPiece.WHITE_PAWN,
            Square.a8.value: ColorChessPiece.BLACK_ROOK,
            Square.e8.value: ColorChessPiece.BLACK_KING
        }

        for square, expected_piece in expected_positions.items():
            self.assertEqual(self.chess_board.get_piece_on_square(square), expected_piece)

    def test_invalid_move(self):
        """Ensure an invalid move raises an error."""
        with self.assertRaises(ValueError):
            self.chess_board._generate_move_board_state(Square.e2.value,
                                                        Square.e5.value)  # Pawn can't jump 3 squares

    def test_piece_movement(self):
        """Ensure moving a piece updates the board state correctly."""
        new_board = ChessBoard(
            board_state=self.chess_board._generate_move_board_state(Square.e2.value, Square.e4.value)
        )
        self.assertEqual(new_board.get_piece_on_square(Square.e4.value), ColorChessPiece.WHITE_PAWN)
        self.assertIsNone(new_board.get_piece_on_square(Square.e2.value))

    def test_capture_piece(self):
        """Ensure capturing a piece removes it from the board."""
        board = ChessBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        board = ChessBoard(board_state=board._generate_move_board_state(Square.e2.value, Square.e4.value))
        board = ChessBoard(board_state=board._generate_move_board_state(Square.d7.value, Square.d5.value))
        board = ChessBoard(board_state=board._generate_move_board_state(Square.e4.value, Square.d5.value))

        self.assertEqual(board.get_piece_on_square(Square.d5.value), ColorChessPiece.WHITE_PAWN)
        self.assertIsNone(board.get_piece_on_square(Square.e4.value))

    def test_pawn_promotion(self):
        """Ensure pawns promote correctly."""
        board = ChessBoard("8/4P3/8/8/8/8/8/k6K w - - 0 1")
        new_board = ChessBoard(board_state=board._generate_move_board_state(Square.e7.value, Square.e8.value))
        self.assertEqual(new_board.get_piece_on_square(Square.e8.value),
                         ColorChessPiece.WHITE_QUEEN)

    def test_en_passant_failure(self):
        """Ensure en passant cannot be performed when conditions are not met."""
        self.chess_board = ChessBoard("rnbqkbnr/pppp1ppp/8/4pP2/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 3")
        with self.assertRaises(ValueError):
            self.chess_board = ChessBoard(
                board_state=self.chess_board._generate_move_board_state(Square.f5.value, Square.e6.value))

        self.assertFalse(self.is_piece_on_square(ColorChessPiece.WHITE_PAWN, Square.e6.value))
        self.assertTrue(self.is_piece_on_square(ColorChessPiece.BLACK_PAWN, Square.e5.value))

    def test_stalemate_detection(self):
        """Ensure stalemate is correctly detected."""
        board = ChessBoard("7k/5Q2/8/8/8/8/8/7K b - - 4 3")
        self.assertEqual(board.check_game_status(board.board_state), GameStatus.STALEMATE)

    def test_fifty_move_rule_draw(self):
        """Ensure the 50-move rule results in a draw."""
        board_state = self.chess_board.board_state
        board_state = replace(board_state, fifty_move_rule=50)
        new_board = ChessBoard(board_state=board_state)
        self.assertEqual(new_board.check_game_status(new_board.board_state),
                         GameStatus.DRAW_50_MOVE)


if __name__ == "__main__":
    unittest.main()
