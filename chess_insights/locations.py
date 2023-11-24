class Locations:
    def __init__(self):
        self.all_pieces = 0
        self.white_pieces = 0
        self.black_pieces = 0
        self.white_pawns = 0
        self.white_knights = 0
        self.white_bishops = 0
        self.white_rooks = 0
        self.white_queens = 0
        self.white_king = 0
        self.black_pawns = 0
        self.black_knights = 0
        self.black_bishops = 0
        self.black_rooks = 0
        self.black_queens = 0
        self.black_king = 0

    def is_square_occupied(self, square) -> bool:
        return self.__is_white_pawn_on_square(square)

    def __is_white_pawn_on_square(self, square) -> bool:
        return self.white_pawns & 2 ** square == 2 ** square

    @staticmethod
    def is_starting_rank(pawn_square) -> bool:
        return 8 <= pawn_square <= 15

    def get_white_pawns(self):
        return self.white_pawns
