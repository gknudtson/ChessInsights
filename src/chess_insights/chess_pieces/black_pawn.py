from .chess_piece import ChessPiece
from chess_insights.game.chess_board import ChessBoard
from chess_insights.util.enum_ray_direction import Direction


class BlackPawn(ChessPiece):
    def __init__(self, chess_board: ChessBoard):
        super().__init__(chess_board)
        self.__is_valid_move = False

    def move(self, origin_square: int, target_square: int):
        move_direction = Direction.from_squares(origin_square, target_square).value[0]
        if self.chess_board.is_whites_turn():
            return
        if not self.chess_board.is_piece_on_square("black", "pawn", origin_square):
            return
        if target_square > 63 or target_square < 0:
            return

        if (move_direction == 'SW' or move_direction == 'SE') and origin_square - target_square <= 9:
            self.capture(target_square)
        elif move_direction == 'S' and origin_square - target_square <= 16:
            self.push(origin_square, target_square)

        if self.__is_valid_move:
            self.__is_valid_move = False
            self.chess_board.add_piece("black", "pawn", target_square)
            self.chess_board.remove_piece("black", "pawn", origin_square)
            self.chess_board.change_turn()

    def capture(self, target_square: int):
        if self.chess_board.is_piece_on_square("white", "piece", target_square):
            self.chess_board.remove_piece_by_square("white", target_square)
            self.__is_valid_move = True
        elif target_square == self.chess_board.en_passant_target_square:
            self.en_passant(target_square)
        if self.__is_valid_move:
            self.chess_board.en_passant_target_square = None

    def en_passant(self, target_square: int):
        self.chess_board.remove_piece("white", "pawn", target_square + 8)
        self.__is_valid_move = True

    def push(self, origin_square: int, target_square: int):
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


