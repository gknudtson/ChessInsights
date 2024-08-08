from enum import Enum

from chess_insights.util.enum_ray_direction import Direction


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
            'white_kings': 0,
            'black_pawns': 0,
            'black_knights': 0,
            'black_bishops': 0,
            'black_rooks': 0,
            'black_queens': 0,
            'black_kings': 0,
        }
        self.__piece_keys_by_color = {
            'white': ['white_pawns', 'white_knights', 'white_bishops', 'white_rooks',
                      'white_queens', 'white_kings'],
            'black': ['black_pawns', 'black_knights', 'black_bishops', 'black_rooks',
                      'black_queens', 'black_kings']
        }
        # left 2 bits represent whites ability to castle left or right, right 2 bits represent black
        self.__castling_rights = 0b1111

    def get_piece_locations(self, color: str, piece: str) -> int:
        piece_key = f"{color}_{piece}s"
        return self.__piece_locations.get(piece_key, 0)

    def is_whites_turn(self) -> bool:
        return self.__is_whites_turn

    def change_turn(self):
        self.__is_whites_turn = not self.is_whites_turn()

    def is_square_occupied(self, square: int) -> bool:
        self.update_all_pieces()
        return (self.__piece_locations['all_pieces'] & (1 << square)) != 0

    def is_piece_on_square(self, color: str, piece: str, square: int) -> bool:
        piece_locations = self.get_piece_locations(color, piece)
        return (piece_locations & (1 << square)) != 0

    def add_piece(self, color: str, piece: str, square: int):
        piece_key = f"{color}_{piece}s"
        self.__piece_locations[piece_key] |= 1 << square
        self.update_all_pieces()

    def remove_piece(self, color: str, piece: str, square: int):
        piece_key = f"{color}_{piece}s"
        self.__piece_locations[piece_key] &= ~(1 << square)
        self.update_all_pieces()

    def update_all_pieces(self):
        self.update_pieces('white')
        self.update_pieces('black')
        self.__piece_locations['all_pieces'] = self.__piece_locations['white_pieces'] | \
                                               self.__piece_locations['black_pieces']

    def update_pieces(self, color: str):
        self.__piece_locations[f'{color}_pieces'] = 0
        for piece in self.__piece_keys_by_color[color]:
            self.__piece_locations[f'{color}_pieces'] |= self.__piece_locations[piece]

    def find_piece_on_square(self, color: str, square: int) -> str:
        for key in self.__piece_keys_by_color[color]:
            if (self.__piece_locations[key] & (1 << square)) != 0:
                return key
        return ''

    def remove_piece_by_color(self, color: str, square: int):
        piece_key = self.find_piece_on_square(color, square)
        if piece_key:
            self.__piece_locations[piece_key] &= ~(1 << square)
            self.update_all_pieces()

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
            path |= 1 << current
            current += step
        path |= 1 << current
        return path
