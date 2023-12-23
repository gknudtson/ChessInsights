class ChessBoard:
    def __init__(self):
        self.__is_whites_turn = True
        self.__piece_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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

    def is_square_occupied(self, square: int) -> bool:
        self.update_white_pieces()
        self.update_black_pieces()
        self.__all_pieces = self.__white_pieces | self.__black_pieces
        return self.__all_pieces & 2 ** square == 2 ** square

    def is_white_piece_on_square(self, square: int) -> bool:
        self.update_white_pieces()
        return self.__white_pieces & 2 ** square == 2 ** square

    def update_white_pieces(self):
        self.__white_pieces = self.__white_pawns | self.__white_knights | self.__white_bishops | self.__white_rooks | \
                              self.__white_queens | self.__white_king

    def is_black_piece_on_square(self, square: int) -> bool:
        self.update_black_pieces()
        return self.__black_pieces & 2 ** square == 2 ** square

    def update_black_pieces(self):
        self.__black_pieces = self.__black_pawns | self.__black_knights | self.__black_bishops | self.__black_rooks | \
                              self.__black_queens | self.__black_king

    def is_white_pawn_on_square(self, square: int) -> bool:
        return self.__white_pawns & 2 ** square == 2 ** square

    @staticmethod
    def is_black_pawn_on_starting_rank(pawn_square) -> bool:
        return 48 <= pawn_square <= 55

    def get_white_pawns(self):
        return self.__white_pawns

    def get_black_pawns(self):
        return self.__black_pawns

    def add_white_pawn(self, square: int):
        self.__white_pawns = self.__white_pawns | 1 << square

    def remove_white_pawn(self, square: int):
        self.__white_pawns = self.__white_pawns & ~(1 << square)

    def add_black_pawn(self, square: int):
        self.__black_pawns = self.__black_pawns | 1 << square

    def remove_black_pawn(self, square: int):
        self.__black_pawns = self.__black_pawns & ~(1 << square)

    def remove_piece(self, square: int):
        return
