import unittest
from parameterized import parameterized
from chess_insights.backend.core.util.enum_ray_direction import Direction
from chess_insights.backend.core.util.enum_chess_piece_type import ColorChessPiece


class TestDirection(unittest.TestCase):

    @parameterized.expand(
        [
            (18, 10, Direction.S),
            (18, 26, Direction.N),
            (18, 27, Direction.NE),
            (18, 11, Direction.SE),
            (18, 9, Direction.SW),
            (18, 25, Direction.NW),
            (18, 19, Direction.E),
            (18, 17, Direction.W),
            (18, 18, Direction.C),
        ]
    )
    def test_ray_direction(self, origin_square, target_square, expected_result):
        self.assertEqual(Direction.from_squares(origin_square, target_square), expected_result)

    @parameterized.expand(
        [
            (ColorChessPiece.WHITE_BISHOP, [Direction.NE, Direction.NW]),
            (ColorChessPiece.BLACK_BISHOP, [Direction.NE, Direction.NW]),
            (ColorChessPiece.WHITE_ROOK, [Direction.N, Direction.E]),
            (ColorChessPiece.BLACK_ROOK, [Direction.N, Direction.E]),
            (ColorChessPiece.WHITE_QUEEN, [Direction.NE, Direction.NW, Direction.N, Direction.E]),
            (ColorChessPiece.BLACK_QUEEN, [Direction.NE, Direction.NW, Direction.N, Direction.E]),
        ]
    )
    def test_get_directions(self, piece, expected_directions):
        self.assertEqual(Direction.get_directions(piece), expected_directions)

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            Direction.from_squares(18, -5)

    def test_invalid_piece(self):
        with self.assertRaises(ValueError):
            Direction.get_directions(ColorChessPiece.WHITE_KNIGHT)


if __name__ == '__main__':
    unittest.main()
