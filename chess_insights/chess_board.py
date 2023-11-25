class ChessBoard:
    def __init__(self):
        self.__is_whites_turn = True
        self.__all_pieces = 0
        self.__white_pieces = 0
        self.__black_pieces = 0
        self.__white_pawns = 0
        self.__white_knights = 0
        self.__white_bishops = 0
        self.__white_rooks = 0
        self.__white_queens = 0
        self.__white_king = 0
        self.__black_pawns = 0
        self.__black_knights = 0
        self.__black_bishops = 0
        self.__black_rooks = 0
        self.__black_queens = 0
        self.__black_king = 0

    def is_whites_turn(self) -> bool:
        return self.__is_whites_turn

    def change_turn(self):
        self.__is_whites_turn = not self.is_whites_turn()

    def is_square_occupied(self, square) -> bool:
        return self.is_white_pawn_on_square(square)

    def is_white_pawn_on_square(self, square) -> bool:
        return self.__white_pawns & 2 ** square == 2 ** square

    @staticmethod
    def is_white_pawn_on_starting_rank(pawn_square) -> bool:
        return 8 <= pawn_square <= 15

    def get_white_pawns(self):
        return self.__white_pawns

    def add_white_pawn(self, square: int):
        self.__white_pawns = self.__white_pawns | 1 << square

    def remove_white_pawn(self, square):
        self.__white_pawns = self.__white_pawns & ~(1 << square)
