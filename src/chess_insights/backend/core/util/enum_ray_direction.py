from enum import Enum

from chess_insights.backend.core.util.enum_chess_piece_type import ColorChessPiece


# Second value is the change in square number based on movement direction
class Direction(Enum):
    N = ('N', 8)
    S = ('S', -8)
    E = ('E', 1)
    W = ('W', -1)
    NE = ('NE', 9)
    NW = ('NW', 7)
    SE = ('SE', -7)
    SW = ('SW', -9)
    C = ('', 0)

    @staticmethod
    def from_squares(origin_square: int, target_square: int) -> Enum:
        if 63 < origin_square < 0 or 63 < target_square < 0:
            raise ValueError('Square must be between 0 and 63')

        square_difference = target_square - origin_square
        if square_difference == 0:
            return Direction.C
        if square_difference % 8 == 0:
            return Direction.N if square_difference > 0 else Direction.S
        elif square_difference % 9 == 0:
            return Direction.NE if square_difference > 0 else Direction.SW
        elif square_difference % 7 == 0:
            return Direction.NW if square_difference > 0 else Direction.SE
        elif square_difference > 0:
            return Direction.E if ((1 << 8) - 1 << (origin_square // 8) * 8) & (
                    1 << target_square) != 0 else Direction.C
        elif square_difference < 0:
            return Direction.W if ((1 << 8) - 1 << (origin_square // 8) * 8) & (
                    1 << target_square) != 0 else Direction.C

    @staticmethod
    def get_directions(piece: ColorChessPiece) -> list:
        if piece == ColorChessPiece.WHITE_BISHOP or piece == ColorChessPiece.BLACK_BISHOP:
            return [Direction.NE, Direction.NW]
        elif piece == ColorChessPiece.WHITE_ROOK or piece == ColorChessPiece.BLACK_ROOK:
            return [Direction.N, Direction.E]
        elif piece == ColorChessPiece.WHITE_QUEEN or piece == ColorChessPiece.BLACK_QUEEN:
            return [Direction.NE, Direction.NW, Direction.N, Direction.E]
        else:
            raise ValueError(f"Invalid piece type: {piece}")
