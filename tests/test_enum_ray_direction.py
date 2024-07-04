import unittest
from parameterized import parameterized

from chess_insights.enum_ray_direction import Direction


class TestChessPieceParentClass(unittest.TestCase):
    @parameterized.expand(
        [(0, Direction.SW), (2, Direction.S), (4, Direction.SE), (9, Direction.SW),
         (10, Direction.S), (11, Direction.SE),
         (16, Direction.W), (17, Direction.W), (18, Direction._), (19, Direction.E), (20, Direction.E),
         (25, Direction.NW), (26, Direction.N), (27, Direction.NE), (32, Direction.NW),
         (33, Direction._), (34, Direction.N), (36, Direction.NE)])
    def test_ray_direction(self, target_square, expected_result):
        origin_square = 18
        assert Direction.from_squares(origin_square, target_square) == expected_result
