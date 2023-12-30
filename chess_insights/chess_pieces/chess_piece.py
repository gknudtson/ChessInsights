from chess_insights.chess_board import ChessBoard


class ChessPiece:

    def __init__(self, chess_board: ChessBoard):
        self.chess_board = chess_board

    def move(self, pawn_square, square_to_move):
        pass

    def direction_classifier(self, piece_square, square_to_move) -> str:
        if (square_to_move - piece_square) % 8 == 0:
            return 'north'
        elif abs(square_to_move - piece_square) % 2 == 0:
            return 'horizontal'
