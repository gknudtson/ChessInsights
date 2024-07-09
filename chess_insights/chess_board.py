from enum import Enum

from chess_insights.enum_ray_direction import Direction
from chess_insights.enum_file_and_rank import *


class ChessBoard:  # TODO check logic for when to update piece locations to increase efficiency
    def __init__(self):
        self.__is_whites_turn = True
        self.en_passant_target_square = None  # TODO: refactor to -1 possibly private
        self.__piece_locations = {
            'all_pieces': 0,
            'white_pieces': 0,
            'black_pieces': 0,
            'white_pawns': 0,
            'white_knights': 0,
            'white_bishops': 0,
            'white_rooks': 0,
            'white_queens': 0,
            'white_king': 0,
            'black_pawns': 0,
            'black_knights': 0,
            'black_bishops': 0,
            'black_rooks': 0,
            'black_queens': 0,
            'black_king': 0,
        }
        self.__piece_keys_by_color = {
            'white': ['white_pawns', 'white_knights', 'white_bishops', 'white_rooks',
                      'white_queens', 'white_king'],
            'black': ['black_pawns', 'black_knights', 'black_bishops', 'black_rooks',
                      'black_queens', 'black_king']
        }
        # left 2 bits represent whites ability to castle left or right, right 2 bits represent black
        self.__castling_rights = 0b1111

    def is_whites_turn(self) -> bool:
        return self.__is_whites_turn

    def change_turn(self):
        self.__is_whites_turn = not self.is_whites_turn()

    def is_square_occupied(self, square: int) -> bool:
        self.update_all_pieces()
        return self.__piece_locations['all_pieces'] & 2 ** square == 2 ** square

    def is_white_piece_on_square(self, square: int) -> bool:
        self.update_white_pieces()
        return self.__piece_locations['white_pieces'] & 2 ** square == 2 ** square

    def update_all_pieces(self):
        self.update_white_pieces()
        self.update_black_pieces()
        self.__piece_locations['all_pieces'] = self.__piece_locations['white_pieces'] | \
                                               self.__piece_locations['black_pieces']

    def update_white_pieces(self):
        self.__piece_locations['white_pieces'] = (
                self.__piece_locations['white_pawns'] |
                self.__piece_locations['white_knights'] |
                self.__piece_locations['white_bishops'] |
                self.__piece_locations['white_rooks'] |
                self.__piece_locations['white_queens'] |
                self.__piece_locations['white_king']
        )

    def is_black_piece_on_square(self, square: int) -> bool:
        self.update_black_pieces()
        return self.__piece_locations['black_pieces'] & 2 ** square == 2 ** square

    def update_black_pieces(self):
        self.__piece_locations['black_pieces'] = (
                self.__piece_locations['black_pawns'] |
                self.__piece_locations['black_knights'] |
                self.__piece_locations['black_bishops'] |
                self.__piece_locations['black_rooks'] |
                self.__piece_locations['black_queens'] |
                self.__piece_locations['black_king']
        )

    def find_white_piece_on_square(self, square: int) -> str:
        for key in self.__piece_keys_by_color['white']:
            if self.__piece_locations[key] & 2 ** square == 2 ** square:
                return key

    def remove_white_piece(self, square: int):
        key = self.find_white_piece_on_square(square)
        self.__piece_locations[key] &= ~(1 << square)
        self.update_all_pieces()

    def is_white_king_on_square(self, square: int) -> bool:
        return self.__piece_locations['white_king'] & 2 ** square == 2 ** square

    def add_white_king(self, square: int):
        self.__piece_locations['white_king'] |= 1 << square
        self.update_all_pieces()

    def remove_white_king(self, square: int):
        self.__piece_locations['white_king'] &= ~(1 << square)
        self.update_all_pieces()

    def is_white_rook_on_square(self, square: int) -> bool:
        return self.__piece_locations['white_rooks'] & 2 ** square == 2 ** square

    def add_white_rook(self, square: int):
        self.__piece_locations['white_rooks'] |= 1 << square
        self.update_all_pieces()

    def remove_white_rook(self, square: int):
        self.__piece_locations['white_rooks'] &= ~(1 << square)
        self.update_all_pieces()

    def is_white_bishop_on_square(self, square: int) -> bool:
        return self.__piece_locations['white_bishops'] & 2 ** square == 2 ** square

    def add_white_bishop(self, square: int):
        self.__piece_locations['white_bishops'] |= 1 << square
        self.update_all_pieces()

    def remove_white_bishop(self, square: int):
        self.__piece_locations['white_bishops'] &= ~(1 << square)
        self.update_all_pieces()

    def is_white_knight_on_square(self, square: int) -> bool:
        return self.__piece_locations['white_knights'] & 2 ** square == 2 ** square

    def add_white_knight(self, square: int):
        self.__piece_locations['white_knights'] |= 1 << square
        self.update_all_pieces()

    def remove_white_knight(self, square: int):
        self.__piece_locations['white_knights'] &= ~(1 << square)
        self.update_all_pieces()

    def is_white_pawn_on_square(self, square: int) -> bool:
        return self.__piece_locations['white_pawns'] & 2 ** square == 2 ** square

    def get_white_pawns(self):
        return self.__piece_locations['white_pawns']

    def add_white_pawn(self, square: int):
        self.__piece_locations['white_pawns'] |= 1 << square
        self.update_all_pieces()

    def remove_white_pawn(self, square: int):
        self.__piece_locations['white_pawns'] &= ~(1 << square)
        self.update_all_pieces()

    def is_black_rook_on_square(self, square: int) -> bool:
        return self.__piece_locations['black_rooks'] & 2 ** square == 2 ** square

    def add_black_rook(self, square: int):
        self.__piece_locations['black_rooks'] |= 1 << square
        self.update_all_pieces()

    def remove_black_rook(self, square: int):
        self.__piece_locations['black_rooks'] &= ~(1 << square)
        self.update_all_pieces()

    def is_black_bishop_on_square(self, square: int) -> bool:
        return self.__piece_locations['black_bishops'] & 2 ** square == 2 ** square

    def add_black_bishop(self, square: int):
        self.__piece_locations['black_bishops'] |= 1 << square
        self.update_all_pieces()

    def remove_black_bishop(self, square: int):
        self.__piece_locations['black_bishops'] &= ~(1 << square)
        self.update_all_pieces()

    def is_black_pawn_on_square(self, square: int) -> bool:
        return self.__piece_locations['black_pawns'] & 2 ** square == 2 ** square

    def get_black_pawns(self):
        return self.__piece_locations['black_pawns']

    def add_black_pawn(self, square: int):
        self.__piece_locations['black_pawns'] |= 1 << square
        self.update_all_pieces()

    def remove_black_pawn(self, square: int):
        self.__piece_locations['black_pawns'] &= ~(1 << square)
        self.update_all_pieces()

    def remove_black_piece(self, square: int):
        key = self.find_black_piece_on_square(square)
        self.__piece_locations[key] &= ~(1 << square)
        self.update_all_pieces()

    def find_black_piece_on_square(self, square: int) -> str:
        for key in self.__piece_keys_by_color['black']:
            if self.__piece_locations[key] & 2 ** square == 2 ** square:
                return key

    def get_castling_rights(self) -> int:
        return self.__castling_rights

    def update_castling_rights(self, new_value: int):
        self.__castling_rights = new_value

    def is_piece_in_path(self, origin_square: int, target_square: int) -> bool:
        direction = Direction.from_squares(origin_square, target_square)
        path = ChessBoard.generate_path(origin_square, target_square, direction)
        return (path & self.__piece_locations['all_pieces']) != 0

    @staticmethod
    def generate_path(origin_square: int, target_square: int, direction: Enum) -> int:
        path = 0
        step = direction.value[1]
        if step == 0:
            return path
        current = origin_square + step
        while current != target_square:
            path |= 2 ** current
            current += step
        path |= 2 ** current
        return path

    def generate_pawn_attacks(self, color: str) -> int:
        a_file = File.A.value
        h_file = File.H.value
        if color == "white":
            pawns = self.__piece_locations["white_pawns"]
            east_attacks = (pawns & ~h_file) << 9
            west_attacks = (pawns & ~a_file) << 7
        elif color == "black":
            pawns = self.__piece_locations["black_pawns"]
            east_attacks = (pawns & ~h_file) >> 7
            west_attacks = (pawns & ~a_file) >> 9
        else:
            return -1

        return east_attacks | west_attacks

    def generate_knight_attacks(self, color: str) -> int:
        if color == "white":
            knights = self.__piece_locations["white_knights"]
        elif color == "black":
            knights = self.__piece_locations["black_knights"]
        else:
            return -1

        a_file = File.A.value
        b_file = File.B.value
        g_file = File.G.value
        h_file = File.H.value
        rank_1 = Rank.One.value
        rank_2 = Rank.Two.value
        rank_7 = Rank.Seven.value
        rank_8 = Rank.Eight.value

        nne = (knights & ~(rank_7 | rank_8 | h_file)) << 17
        nee = (knights & ~(rank_8 | h_file | g_file)) << 10
        nnw = (knights & ~(rank_7 | rank_8 | a_file)) << 15
        nww = (knights & ~(rank_8 | a_file | g_file)) << 6
        sse = (knights & ~(rank_1 | rank_2 | h_file)) >> 15
        see = (knights & ~(rank_1 | g_file | h_file)) >> 6
        ssw = (knights & ~(rank_1 | rank_2 | a_file)) >> 10
        sww = (knights & ~(rank_1 | a_file | b_file)) >> 17

        return nne | nee | nnw | nww | sse | see | ssw | sww

    # TODO needs to consider all squares attacked by opponent pieces
    def generate_king_attacks(self, color: str) -> int:
        a_file = File.A.value
        h_file = File.H.value
        rank_1 = Rank.One.value
        rank_8 = Rank.Eight.value
        if color == "white":
            king = self.__piece_locations["white_king"]
        elif color == "black":
            king = self.__piece_locations["black_king"]
        else:
            return -1
        east = (king & ~h_file) << 1
        west = (king & ~a_file) >> 1
        north = (king & ~rank_8) << 8
        south = (king & ~rank_1) >> 8
        ne = (north & ~h_file) << 1
        nw = (north & ~a_file) >> 1
        se = (south & ~h_file) << 1
        sw = (south & ~a_file) >> 1

        return east | west | north | south | ne | nw | se | sw
