import unittest

from parameterized import parameterized

from chess_insights.game.castling import get_castling_moves, update_castling_rights
from chess_insights.engine.bitboard import BitBoard
from chess_insights.util.enum_chess_piece_type import Color, ChessPieceType
from chess_insights.util.enum_square import Square


class TestKing(unittest.TestCase):

    @parameterized.expand([[Color.WHITE, 68], [Color.BLACK, 4899916394579099648]])
    def test_get_castling_moves_empty_board(self, color, expected):
        assert get_castling_moves(color, 0b1111, BitBoard(), BitBoard()).board == expected

    @parameterized.expand([[Color.WHITE, 0], [Color.BLACK, 0]])
    def test_get_castling_moves_no_rights(self, color, expected):
        assert get_castling_moves(color, 0b0000, BitBoard(), BitBoard()).board == expected

    @parameterized.expand(
        [[Color.WHITE, 65425, 68], [Color.BLACK, 10520127254560768000, 4899916394579099648]])
    def test_get_castling_moves_no_collisions(self, color, collisions, expected):
        assert get_castling_moves(color, 0b1111, BitBoard(), BitBoard(collisions)).board == expected

    @parameterized.expand(
        [[Color.WHITE, 147, 64], [Color.BLACK, 12754194144713244672, 288230376151711744]])
    def test_get_castling_moves_collisions(self, color, collisions, expected):
        assert get_castling_moves(color, 0b1111, BitBoard(), BitBoard(collisions)).board == expected

    @parameterized.expand(
        [[Color.WHITE, 144680345676218114, 68],
         [Color.BLACK, 144680345676218114, 4899916394579099648]])
    def test_get_castling_moves_no_attacks(self, color, attacks, expected):
        assert get_castling_moves(color, 0b1111, BitBoard(attacks), BitBoard()).board == expected

    @parameterized.expand(
        [[Color.WHITE, 4, 64],
         [Color.BLACK, 2305843009213693952, 288230376151711744]])
    def test_get_castling_moves_attacks(self, color, attacks, expected):
        assert get_castling_moves(color, 0b1111, BitBoard(attacks), BitBoard()).board == expected

    @parameterized.expand(
        [[Color.WHITE, 16, 0],
         [Color.BLACK, 1152921504606846976, 0]])
    def test_get_castling_moves_under_check(self, color, attacks, expected):
        assert get_castling_moves(color, 0b1111, BitBoard(attacks), BitBoard()).board == expected

    @parameterized.expand([
        [Color.WHITE, 0b1000, 64],  # White, kingside rights only -> only short castle
        [Color.WHITE, 0b0100, 4],  # White, queenside rights only -> only long castle
        [Color.BLACK, 0b0010, 4611686018427387904],  # Black, kingside rights only -> only short castle
        [Color.BLACK, 0b0001, 288230376151711744],  # Black, queenside rights only -> only long castle
    ])
    def test_get_castling_moves_asymmetric_rights(self, color, castling_rights, expected):
        # Regression: castle_short/castle_long must not read each other's bit.
        assert get_castling_moves(color, castling_rights, BitBoard(), BitBoard()).board == expected

    @parameterized.expand([
        [Color.WHITE, Square.e1.value, 0b0011],
        [Color.BLACK, Square.e8.value, 0b1100],
    ])
    def test_update_castling_rights_king(self, color, square, expected):
        piece = color.get_color_piece_by_type(ChessPieceType.KING)

        assert update_castling_rights(0b1111, piece, square) == expected

    @parameterized.expand([
        [Color.WHITE, Square.a1.value, 0b1011],
        [Color.WHITE, Square.h1.value, 0b0111],
        [Color.BLACK, Square.a8.value, 0b1110],
        [Color.BLACK, Square.h8.value, 0b1101],
    ])
    def test_update_castling_rights_rook(self, color, square, expected):
        piece = color.get_color_piece_by_type(ChessPieceType.ROOK)

        assert update_castling_rights(0b1111, piece, square) == expected

    @parameterized.expand([
        [Color.WHITE, Square.a2.value],
        [Color.BLACK, Square.h7.value],
    ])
    def test_update_castling_rights_rook_non_starting_square(self, color, square):
        piece = color.get_color_piece_by_type(ChessPieceType.ROOK)

        assert update_castling_rights(0b1111, piece, square) == 0b1111

    @parameterized.expand([
        [Color.WHITE, Square.b1.value],
        [Color.BLACK, Square.b8.value],
    ])
    def test_update_castling_rights_other_piece(self, color, square):
        piece = color.get_color_piece_by_type(ChessPieceType.KNIGHT)

        assert update_castling_rights(0b1111, piece, square) == 0b1111