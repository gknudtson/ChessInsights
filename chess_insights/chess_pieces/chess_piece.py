from chess_insights.chess_board import ChessBoard
from chess_insights.enum_square import Square


class ChessPiece:

    def __init__(self, chess_board: ChessBoard):
        self.chess_board = chess_board

    def move(self, pawn_square: int, square_to_move: int):
        pass

    @staticmethod
    def ray_direction(origin_square: int,
                      target_square: int) -> str:  # TODO consider ENUM
        square_difference = target_square - origin_square
        if square_difference == 0:
            return ''
        if square_difference % 8 == 0:
            return 'N' if square_difference > 0 else 'S'
        elif square_difference % 9 == 0:
            return 'NE' if square_difference > 0 else 'SW'
        elif square_difference % 7 == 0:
            return 'NW' if square_difference > 0 else 'SE'
        elif square_difference > 0:
            return 'E' if ((1 << 8) - 1 << (origin_square // 8) * 8) & (1 << target_square) != 0 else ''
        elif square_difference < 0:
            return 'W' if ((1 << 8) - 1 << (origin_square // 8) * 8) & (1 << target_square) != 0 else ''

    @staticmethod
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
