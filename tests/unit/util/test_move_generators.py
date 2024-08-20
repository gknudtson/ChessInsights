import unittest

from chess_insights.util.move_generators import *


class TestMoveGenerators(unittest.TestCase):
    def test_generate_rook_attacks(self):
        assert get_sliding_attacks(268435457, 268435457, "rook") == 1229782941971845630

    def test_generate_rook_attacks_with_collisions(self):
        assert get_sliding_attacks(2516582675, 268435457, "rook") == 1157442769100214546

    def test_generate_rook_attacks_with_collisions_v2(self):
        assert get_sliding_attacks(1442840851, 268435457, "rook") == 1157442766952730898

    def test_generate_queen_attacks(self):
        assert get_sliding_attacks(268435456, 268435456, "queen") == 1266167048752878738

    def test_generate_queen_attacks_two_queens(self):
        assert get_sliding_attacks(268435457, 268435457, "queen") == 10507871247272859646

    def test_generate_queen_attacks_with_collisions(self):
        assert get_sliding_attacks(9259475670827270547, 9223372037123211265,
                                   "queen") == 9205467831842132882

    def test_generate_pawn_attacks_white(self):
        assert generate_pawn_attacks(37120, "white") == 6946816

    def test_generate_pawn_attacks_black(self):
        assert (generate_pawn_attacks(40813871623045120, "black") == 116548232544256)

    def test_generate_king_attacks_white_centered(self):
        assert generate_king_attacks(1024) == 920078

    def test_generate_king_attacks_white_corners(self):
        assert generate_king_attacks(9295429630892703873) == 4810688826961871682

    def test_generate_knight_attacks_white(self):
        assert generate_knight_attacks(1048576) == 172939559976

    def test_generate_knight_attacks_white_corners(self):
        assert generate_knight_attacks(9295429630892703873) == 10205666933351424

    def test_generate_bishop_attacks(self):
        assert get_sliding_attacks(1572864, 1572864, "bishop") == 36525115856403558

    def test_generate_bishop_attacks_with_collisions(self):
        assert get_sliding_attacks(566937257984, 1572864, "bishop") == 36241441856437346
