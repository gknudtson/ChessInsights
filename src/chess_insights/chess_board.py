from enum import Enum

from chess_insights.util.enum_ray_direction import Direction
from chess_insights.util.move_generators import generate_pawn_attacks, generate_knight_attacks, \
    generate_king_attacks, get_sliding_attacks


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

    def setup(self):
        self.__piece_locations["all_pieces"] = 18446462598732906495
        self.__piece_locations["white_pieces"] = 65535
        self.__piece_locations["black_pieces"] = 18446462598732840960
        self.__piece_locations["white_pawns"] = 65280
        self.__piece_locations["white_knights"] = 66
        self.__piece_locations["white_bishops"] = 36
        self.__piece_locations["white_rooks"] = 129
        self.__piece_locations["white_queens"] = 8
        self.__piece_locations["white_kings"] = 16
        self.__piece_locations["black_pawns"] = 71776119061217280
        self.__piece_locations["black_knights"] = 4755801206503243776
        self.__piece_locations["black_bishops"] = 2594073385365405696
        self.__piece_locations["black_rooks"] = 9295429630892703744
        self.__piece_locations["black_queens"] = 576460752303423488
        self.__piece_locations["black_kings"] = 1152921504606846976

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

    def get_moves(self, piece_key: str, color: str, square: int):
        piece = piece_key.split('_')[1]
        match piece:
            case "pawns":
                return generate_pawn_attacks(square, color)
            case "knights":
                return generate_knight_attacks(square)
            case "kings":
                return generate_king_attacks(square)
            case "bishops" | "rooks" | "queens":
                return get_sliding_attacks(self.__piece_locations["all_pieces"],
                                           square, piece)
            case _:
                raise ValueError(f"Incorrect piece type passed to move_generator")

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
