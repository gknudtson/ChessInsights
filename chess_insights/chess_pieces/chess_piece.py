from chess_insights.chess_board import ChessBoard
from chess_insights.enum_square import Square


class ChessPiece:

    def __init__(self, chess_board: ChessBoard):
        self.chess_board = chess_board

    def move(self, pawn_square: int, square_to_move: int):
        pass

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
