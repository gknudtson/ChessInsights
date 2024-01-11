import unittest
from parameterized import parameterized
from chess_insights.chess_pieces.chess_piece import ChessPiece


class TestChessPieceParentClass(unittest.TestCase):
    def setUp(self):
        self.chess_piece = ChessPiece

    @parameterized.expand(
        [(0, 'SW'), (2, 'S'), (4, 'SE'), (9, 'SW'), (10, 'S'), (11, 'SE'), (16, 'W'), (17, 'W'), (18, ''), (19, 'E'),
         (20, 'E'),
         (25, 'NW'), (26, 'N'), (27, 'NE'), (32, 'NW'), (33, ''), (34, 'N'), (36, 'NE')])
    def test_ray_direction(self, target_square, expected_result):
        origin_square = 18
        assert self.chess_piece.ray_direction(origin_square, target_square) == expected_result
