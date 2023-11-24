from chess_insights.chess_board import ChessBoard


class ChessPiece:
    chess_board = None

    def __init__(self):
        if ChessPiece.chess_board is None:
            raise ValueError("ChessBoard is not set. Call set_chess_board to set it.")

    @classmethod
    def set_chess_board(cls, chess_board: ChessBoard):
        cls.chess_board = chess_board

    def move(self, pawn_square, square_to_move):
        pass
