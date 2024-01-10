from chess_insights.chess_pieces.chess_piece import ChessPiece
from chess_insights.chess_board import ChessBoard


class BlackPawn(ChessPiece):
    def __init__(self, chess_board: ChessBoard):
        super().__init__(chess_board)
        self.__is_valid_move = False

    def movement_manager(self, pawn_square: int, square_to_move: int):
        move_direction = self.ray_direction(pawn_square, square_to_move)
        if self.chess_board.is_whites_turn():
            return
        if not self.chess_board.is_black_pawn_on_square(pawn_square):
            return
        if square_to_move > 63 or square_to_move < 0:
            return

        if (move_direction == 'SW' or move_direction == 'SE') and pawn_square - square_to_move <= 9:
            self.capture(square_to_move)
        elif move_direction == 'S' and pawn_square - square_to_move <= 16:
            self.move(pawn_square, square_to_move)

        if self.__is_valid_move:
            self.__is_valid_move = False
            self.chess_board.add_black_pawn(square_to_move)
            self.chess_board.remove_black_pawn(pawn_square)
            self.chess_board.change_turn()

    def capture(self, square_to_move: int):
        if self.chess_board.is_white_piece_on_square(square_to_move):
            self.chess_board.remove_white_piece(square_to_move)
            self.__is_valid_move = True
        elif square_to_move == self.chess_board.en_passant_target_square:
            self.en_passant(square_to_move)
        if self.__is_valid_move:
            self.chess_board.en_passant_target_square = None

    def en_passant(self, square_to_move: int):
        self.chess_board.remove_white_pawn(square_to_move + 8)
        self.__is_valid_move = True

    def move(self, pawn_square: int, square_to_move: int):
        if self.chess_board.is_square_occupied(square_to_move):
            return
        if square_to_move == pawn_square - 8:
            self.__is_valid_move = True
            self.chess_board.en_passant_target_square = None
        elif square_to_move == pawn_square - 16:
            self.double_push(pawn_square)

    def double_push(self, pawn_square: int):
        if self.is_starting_rank(pawn_square) and not self.chess_board.is_square_occupied(pawn_square - 8):
            self.chess_board.en_passant_target_square = pawn_square - 8
            self.__is_valid_move = True

    @staticmethod
    def is_starting_rank(pawn_square) -> bool:
        return 48 <= pawn_square <= 55
