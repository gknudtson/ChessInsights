import numpy as np

from .enum_file_and_rank import Rank, File
from .enum_ray_direction import Direction


def mirror_vertical(bit_board: int) -> int:
    if bit_board < 0:
        bit_board &= 0xFFFFFFFFFFFFFFFF
    bitboard_array = np.array([bit_board], dtype=np.uint64)
    flipped_array = bitboard_array.byteswap()
    return mirror_horizontal(flipped_array.item())


def mirror_horizontal(bitboard):
    # Convert the 64-bit integer to an array of 8 bytes
    bytes_array = np.array([bitboard], dtype=np.uint64).view(np.uint8)
    # Reverse the bits in each byte using bitwise operations
    reversed_bytes = np.array([reverse_bits(byte) for byte in bytes_array],
                              dtype=np.uint8)
    # Combine the reversed bytes back into a 64-bit integer
    mirrored_bitboard = reversed_bytes.view(np.uint64)[0]
    return mirrored_bitboard.item()


def reverse_bits(byte):
    byte = (byte & 0xF0) >> 4 | (byte & 0x0F) << 4
    byte = (byte & 0xCC) >> 2 | (byte & 0x33) << 2
    byte = (byte & 0xAA) >> 1 | (byte & 0x55) << 1
    return byte


def generate_mask(square: int, direction: Direction) -> int:
    if direction == Direction.N or direction == Direction.S:
        return 0x0101010101010101 << get_file(square)
    elif direction == Direction.E or direction == Direction.W:
        return 0xFF << (8 * get_rank(square))
    else:
        return get_diagonal_mask(square, direction)


def get_diagonal_mask(origin_square: int, direction: Direction) -> int:
    return (generate_diagonal_path_to_edge_of_board(origin_square, direction.value[1]) |
            generate_diagonal_path_to_edge_of_board(origin_square, -direction.value[1]))


def generate_diagonal_path_to_edge_of_board(origin_square: int, offset: int) -> int:
    abs_offset = abs(offset)
    start_square = 2 ** origin_square
    edges = Rank.One | Rank.Eight | File.A | File.H
    current_square, path = start_square, start_square

    is_first_iteration = True
    while current_square & edges == 0 or is_first_iteration:
        if offset > 0:
            current_square = current_square << abs_offset
        else:
            current_square = current_square >> abs_offset
        if current_square > 2 ** 63 or current_square == 0:
            break
        path |= current_square
        is_first_iteration = False
    return path


def get_file(square: int) -> int:
    return square % 8


def get_rank(square: int) -> int:
    return square // 8
