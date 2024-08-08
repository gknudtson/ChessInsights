from enum import Enum
from typing import Tuple


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
    _ = ('', 0)  # TODO Possibly name C for Center

    @staticmethod
    def from_squares(origin_square: int,
                     target_square: int) -> Enum:
        square_difference = target_square - origin_square
        if square_difference == 0:
            return Direction._
        if square_difference % 8 == 0:
            return Direction.N if square_difference > 0 else Direction.S
        elif square_difference % 9 == 0:
            return Direction.NE if square_difference > 0 else Direction.SW
        elif square_difference % 7 == 0:
            return Direction.NW if square_difference > 0 else Direction.SE
        elif square_difference > 0:
            return Direction.E if ((1 << 8) - 1 << (origin_square // 8) * 8) & (
                    1 << target_square) != 0 else Direction._
        elif square_difference < 0:
            return Direction.W if ((1 << 8) - 1 << (origin_square // 8) * 8) & (
                    1 << target_square) != 0 else Direction._

    @staticmethod
    def get_directions(piece: str) -> list:
        if piece == "bishop":
            return [Direction.NE, Direction.NW]
        elif piece == "rook":
            return [Direction.N, Direction.E]
        elif piece == "queen":
            return [Direction.NE, Direction.NW, Direction.N, Direction.E]
        else:
            return []
