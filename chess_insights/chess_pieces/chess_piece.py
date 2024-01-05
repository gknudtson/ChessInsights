from chess_insights.chess_board import ChessBoard


class ChessPiece:

    def __init__(self, chess_board: ChessBoard):
        self.chess_board = chess_board

    def movement_manager(self, pawn_square: int, square_to_move: int):  # Potential name change
        pass

    @staticmethod
    def ray_direction(origin_square, target_square) -> str:
        if (target_square - origin_square) % 8 == 0 and (target_square - origin_square) > 0:
            return 'N'
        elif (target_square - origin_square) % 8 == 0 and (target_square - origin_square) < 0:
            return 'S'
        elif (target_square - origin_square) % 9 == 0 and (target_square - origin_square) > 0:
            return 'NE'
        elif (target_square - origin_square) % 7 == 0 and (target_square - origin_square) > 0:
            return 'NW'
        elif (target_square - origin_square) % 9 == 0 and (target_square - origin_square) < 0:
            return 'SE'
        elif (target_square - origin_square) % 7 == 0 and (target_square - origin_square) < 0:
            return 'SW'
        elif (target_square - origin_square) > 0:
            return 'E'
        elif (target_square - origin_square) < 0:
            return 'W'
