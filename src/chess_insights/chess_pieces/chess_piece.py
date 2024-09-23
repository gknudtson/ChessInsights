from chess_insights.game.chess_board import ChessBoard


class ChessPiece:

    def __init__(self, chess_board: ChessBoard):
        self.chess_board = chess_board

    def move(self, pawn_square: int, square_to_move: int):
        pass
