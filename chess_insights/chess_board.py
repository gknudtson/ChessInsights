class ChessBoard:
    def __init__(self):
        self.turn = True
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

    def is_square_occupied(self, square) -> bool:
        return self.__is_white_pawn_on_square(square)

    def __is_white_pawn_on_square(self, square) -> bool:
        return self.__white_pawns & 2 ** square == 2 ** square

    def get_white_pawns(self):
        return self.__white_pawns

    def add_white_pawn(self, square):
        self.__white_pawns = self.__white_pawns | 1 << square

    def remove_white_pawn(self, square):
        self.__white_pawns = self.__white_pawns & ~(1 << square)

    @staticmethod
    def is_starting_rank(pawn_square) -> bool:
        return 8 <= pawn_square <= 15
