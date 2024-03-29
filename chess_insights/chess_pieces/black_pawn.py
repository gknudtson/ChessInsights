from chess_insights.chess_pieces.chess_piece import ChessPiece
from chess_insights.chess_board import ChessBoard


class BlackPawn(ChessPiece):
    def __init__(self, chess_board: ChessBoard):
        super().__init__(chess_board)
        self.__is_valid_move = False

    def movement_manager(self, origin_square: int, target_square: int):
        move_direction = self.ray_direction(origin_square, target_square)
        if self.chess_board.is_whites_turn():
            return
        if not self.chess_board.is_black_pawn_on_square(origin_square):
            return
        if target_square > 63 or target_square < 0:
            return

        if (move_direction == 'SW' or move_direction == 'SE') and origin_square - target_square <= 9:
            self.capture(target_square)
        elif move_direction == 'S' and origin_square - target_square <= 16:
            self.move(origin_square, target_square)

        if self.__is_valid_move:
            self.__is_valid_move = False
            self.chess_board.add_black_pawn(target_square)
            self.chess_board.remove_black_pawn(origin_square)
            self.chess_board.change_turn()

    def capture(self, target_square: int):
        if self.chess_board.is_white_piece_on_square(target_square):
            self.chess_board.remove_white_piece(target_square)
            self.__is_valid_move = True
        elif target_square == self.chess_board.en_passant_target_square:
            self.en_passant(target_square)
        if self.__is_valid_move:
            self.chess_board.en_passant_target_square = None

    def en_passant(self, target_square: int):
        self.chess_board.remove_white_pawn(target_square + 8)
        self.__is_valid_move = True

    def move(self, origin_square: int, target_square: int):
        if self.chess_board.is_square_occupied(target_square):
            return
        if target_square == origin_square - 8:
            self.__is_valid_move = True
            self.chess_board.en_passant_target_square = None
        elif target_square == origin_square - 16:
            self.double_push(origin_square)

    def double_push(self, origin_square: int):
        if self.is_starting_rank(origin_square) and not self.chess_board.is_square_occupied(origin_square - 8):
            self.chess_board.en_passant_target_square = origin_square - 8
            self.__is_valid_move = True

    @staticmethod
    def is_starting_rank(origin_square) -> bool:
        return 48 <= origin_square <= 55
