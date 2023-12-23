from chess_insights.chess_pieces.chess_piece import ChessPiece
from chess_insights.chess_board import ChessBoard


class WhitePawn(ChessPiece):
    def __init__(self, chess_board: ChessBoard):
        super().__init__(chess_board)

    def move(self, pawn_square: int, square_to_move: int):
        if not self.chess_board.is_whites_turn():
            return
        if not self.chess_board.is_white_pawn_on_square(pawn_square):
            return
        if self.chess_board.is_white_piece_on_square(square_to_move) or (self.chess_board.is_black_piece_on_square(
                square_to_move) and not (square_to_move == pawn_square + 9 or square_to_move == pawn_square + 7)):
            return
        if square_to_move == pawn_square + 8:
            self.chess_board.add_white_pawn(square_to_move)
        elif square_to_move == pawn_square + 16 and self.is_starting_rank(
                pawn_square) and not self.chess_board.is_square_occupied(pawn_square + 8):
            self.chess_board.add_white_pawn(square_to_move)
        elif square_to_move == pawn_square + 9 or square_to_move == pawn_square + 7 and \
                self.chess_board.is_black_piece_on_square(square_to_move):
            self.chess_board.add_white_pawn(square_to_move)
            self.chess_board.remove_black_pawn(square_to_move)
        # Need el passante
        self.chess_board.remove_white_pawn(pawn_square)
        self.chess_board.change_turn()

    @staticmethod
    def is_starting_rank(pawn_square: int) -> bool:
        return 8 <= pawn_square <= 15
