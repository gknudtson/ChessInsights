from chess_insights.chess_pieces.chess_piece import ChessPiece
from chess_insights.chess_board import ChessBoard


class WhiteKing(ChessPiece):
    def __init__(self, chess_board: ChessBoard):
        super().__init__(chess_board)
        self.__is_valid_move = False

    def movement_manager(self, origin_square: int, target_square: int):
        move_direction = self.ray_direction(origin_square, target_square)
        move_distance = abs(target_square - origin_square)
        if not self.chess_board.is_whites_turn():
            return
        if not self.chess_board.is_white_king_on_square(origin_square):
            return
        if target_square > 63 or target_square < 0:
            return

        if move_direction == '':
            return
        elif move_distance > 9:
            return
        elif (move_direction == 'E' or move_direction == 'W') and move_distance > 1:
            return

        if self.chess_board.is_black_piece_on_square(target_square):
            self.chess_board.remove_black_piece(target_square)
            self.__is_valid_move = True
        elif not self.chess_board.is_white_piece_on_square(target_square):
            self.__is_valid_move = True

        if self.__is_valid_move:
            self.__is_valid_move = False
            self.chess_board.add_white_king(target_square)
            self.chess_board.remove_white_king(origin_square)
            self.chess_board.change_turn()
