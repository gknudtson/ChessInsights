from chess_insights.util.enum_chess_piece_type import Color
from chess_insights.util.enum_square import Square


def pawn_movement(color: Color, square: int) -> (int, int):
    if color == Color.WHITE:
        return square + 8, square + 16
    elif color == Color.BLACK:
        return square - 8, square - 16


def is_pawn_starting_rank(origin_square: int, color: Color) -> bool:
    if color == Color.WHITE:
        is_starting_rank = 8 <= origin_square <= 15
    elif color == Color.BLACK:
        is_starting_rank = 48 <= origin_square <= 55

    return is_starting_rank


def chebyshev_distance(origin_square: int, target_square: int) -> int:
    if target_square < 0 or origin_square < 0 or target_square > 63 or origin_square > 63:
        return -1
    origin_algebraic_notation = Square(origin_square).name
    target_algebraic_notation = Square(target_square).name
    origin_rank = ord(origin_algebraic_notation[0])
    target_rank = ord(target_algebraic_notation[0])
    origin_file = ord(origin_algebraic_notation[1])
    target_file = ord(target_algebraic_notation[1])
    return max(abs(origin_rank - target_rank), abs(origin_file - target_file))
