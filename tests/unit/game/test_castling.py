import unittest

from parameterized import parameterized

from chess_insights.backend.core.game.castling import get_castling_moves
from chess_insights.backend.core.engine.bitboard import BitBoard
from chess_insights.backend.core.util.enum_chess_piece_type import Color


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
