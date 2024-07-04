from ..chess_pieces.chess_piece import ChessPiece
from ..chess_board import ChessBoard
from ..enum_ray_direction import Direction


class WhiteKing(ChessPiece):
    def __init__(self, chess_board: ChessBoard):
        super().__init__(chess_board)
        self.__is_valid_move = False

    def move(self, origin_square: int, target_square: int):
        move_direction = Direction.from_squares(origin_square, target_square).value[0]
        move_distance = abs(target_square - origin_square)
        castling_rights = self.chess_board.get_castling_rights()
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
        elif (move_direction == 'E' or move_direction == 'W') and move_distance > 2:
            return

        if move_distance == 2:
            self.castle(move_direction,castling_rights)
        elif self.chess_board.is_black_piece_on_square(target_square):
            self.chess_board.remove_black_piece(target_square)
            self.__is_valid_move = True
        elif not self.chess_board.is_white_piece_on_square(target_square):
            self.__is_valid_move = True

        if self.__is_valid_move:
            self.__is_valid_move = False
            self.chess_board.add_white_king(target_square)
            self.chess_board.remove_white_king(origin_square)
            self.chess_board.update_castling_rights(castling_rights & 0b0011) if origin_square == 4 else None
            self.chess_board.change_turn()

    def castle(self, move_direction: str, castling_rights: int):
        if move_direction == 'E' and castling_rights & 0b0100 == 0b0100:
            self.chess_board.add_white_rook(5)
            self.chess_board.remove_white_rook(7)
            self.__is_valid_move = True
        elif move_direction == 'W' and castling_rights & 0b1000 == 0b1000:
            self.chess_board.add_white_rook(3)
            self.chess_board.remove_white_rook(0)
            self.__is_valid_move = True
