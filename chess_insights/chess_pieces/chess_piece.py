from chess_insights.chess_board import ChessBoard


class ChessPiece:

    def __init__(self, chess_board: ChessBoard):
        self.chess_board = chess_board

    def movement_manager(self, pawn_square: int, square_to_move: int):  # TODO Potential name change
        pass

    @staticmethod
    def ray_direction(origin_square: int, target_square: int) -> str:
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
