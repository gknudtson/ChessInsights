from chess_insights.chess_pieces.chess_piece import ChessPiece
from chess_insights.chess_board import ChessBoard


class WhitePawn(ChessPiece):
    def __init__(self):
        super().__init__()

    def move(self, pawn_square, square_to_move):
        if not self.chess_board.turn:
            return
        if not self.__is_white_pawn_on_square(pawn_square):
            return
        if self.chess_board.is_square_occupied(square_to_move):
            return
        if square_to_move == pawn_square + 8:
            self.chess_board.add_white_pawn(square_to_move)
            self.chess_board.turn = False
        elif square_to_move == pawn_square + 16 and self.chess_board.is_starting_rank(
                pawn_square) and not self.chess_board.is_square_occupied(
            pawn_square + 8):
            self.chess_board.add_white_pawn(square_to_move)
            self.chess_board.turn = False

    @staticmethod
    def is_starting_rank(pawn_square) -> bool:
        return 8 <= pawn_square <= 15
