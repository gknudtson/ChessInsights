from .enum_file_and_rank import Rank, File
from .enum_ray_direction import Direction
from ..util.serializers import serialize_board
from .bitboard import mirror_vertical, generate_mask


def get_sliding_attacks(collisions: int, piece_board: int, piece: str) -> int:
    squares = serialize_board(piece_board)
    directions = Direction.get_directions(piece)

    attacks = generate_sliding_attacks(collisions, squares, directions)
    return attacks


def generate_sliding_attacks(collisions: int, squares: list, directions: list) -> int:
    mirrored_collisions = mirror_vertical(collisions)
    attacks = 0
    for square in squares:
        bit_square = 1 << square
        mirrored_square = mirror_vertical(bit_square)
        for direction in directions:
            mask = generate_mask(square, direction)
            mirrored_mask = mirror_vertical(mask)
            positive_path = (collisions & mask) - 2 * bit_square
            negative_path = mirror_vertical(
                (mirrored_collisions & mirrored_mask) - 2 * mirrored_square)
            path = positive_path ^ negative_path
            attacks |= path & mask

    return attacks


def generate_pawn_attacks(pawns: int, color: str) -> int:
    a_file = File.A.value
    h_file = File.H.value
    if color == "white":
        east_attacks = (pawns & ~h_file) << 9
        west_attacks = (pawns & ~a_file) << 7
    elif color == "black":
        east_attacks = (pawns & ~h_file) >> 7
        west_attacks = (pawns & ~a_file) >> 9
    else:
        return -1

    return east_attacks | west_attacks


def generate_knight_attacks(knights: int) -> int:
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
    nww = (knights & ~(rank_8 | a_file | b_file | g_file)) << 6
    sse = (knights & ~(rank_1 | rank_2 | h_file)) >> 15
    see = (knights & ~(rank_1 | g_file | h_file)) >> 6
    ssw = (knights & ~(rank_1 | rank_2 | a_file)) >> 10
    sww = (knights & ~(rank_1 | a_file | b_file)) >> 17

    return nne | nee | nnw | nww | sse | see | ssw | sww


# TODO needs to consider all squares attacked by opponent pieces
def generate_king_attacks(king: int) -> int:
    a_file = File.A.value
    h_file = File.H.value
    rank_1 = Rank.One.value
    rank_8 = Rank.Eight.value

    east = (king & ~h_file) << 1
    west = (king & ~a_file) >> 1
    north = (king & ~rank_8) << 8
    south = (king & ~rank_1) >> 8
    ne = (north & ~h_file) << 1
    nw = (north & ~a_file) >> 1
    se = (south & ~h_file) << 1
    sw = (south & ~a_file) >> 1

    return east | west | north | south | ne | nw | se | sw
