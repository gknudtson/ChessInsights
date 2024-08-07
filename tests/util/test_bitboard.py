import unittest

from chess_insights.util.bitboard import *


class TestBitBoard(unittest.TestCase):
    def test_get_file(self):
        assert get_file(7) == 7

    def test_get_rank(self):
        assert get_rank(7) == 0

    def test_generate_diagonal_path(self):
        assert generate_diagonal_path_to_edge_of_board(0, 9) == 9241421688590303745

    def test_generate_mask(self):
        assert generate_mask(27, Direction.NE) == 9241421688590303745

    def test_mirror_vertical(self):
        assert mirror_vertical(73165767551) == 18356848623779577856
