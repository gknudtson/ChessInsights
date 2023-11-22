class ChessBoard:
    def __init__(self):
        self.turn = True
        self.__white_pawns = 0

    def get_white_pawns(self):
        return self.__white_pawns

    def add_white_pawn(self, square):
        self.__white_pawns = self.__white_pawns | 1 << square

    def remove_white_pawn(self, square):
        self.__white_pawns = self.__white_pawns & ~(1 << square)

    def square_occupied(self, square):
        return self.__white_pawns & 2 ** square == 2 ** square

    def white_pawn_movement(self, pawn_square, square_to_move):
        if not self.turn:
            pass
        elif self.square_occupied(square_to_move):
            pass
        elif square_to_move == pawn_square + 8:
            self.add_white_pawn(square_to_move)
            self.turn = False
