import math
import numpy as np

from chess_insights.backend.core.util.enum_chess_piece_type import ColorChessPiece
from chess_insights.backend.core.util.enum_file_and_rank import Rank, File
from chess_insights.backend.core.util.enum_ray_direction import Direction
from chess_insights.backend.core.util.enum_square import chebyshev_distance


class BitBoard:
    def __init__(self, board: int = 0, board_type: ColorChessPiece = None):
        if not (-(1 << 64) <= board < (1 << 64)):
            raise ValueError(f"Bitboard must be a 64-bit integer. {board} is not")

        self.board = board & 0xFFFFFFFFFFFFFFFF
        self.board_type = board_type

    def set_board(self, board: int):
        if not (0 <= board < (1 << 64)):
            raise ValueError("Bitboard must be a 64-bit integer.")
        self.board = board

    def set_bit(self, square: int):
        """Set a bit at the given square (0-63)."""
        if not (0 <= square < 64):
            raise ValueError("Square must be between 0 and 63.")
        self.board |= (1 << square)

    def clear_bit(self, square: int):
        """Clear a bit at the given square (0-63)."""
        if not (0 <= square < 64):
            raise ValueError("Square must be between 0 and 63.")
        self.board &= ~(1 << square)

    def serialize_board(self) -> list[int]:
        board = self.board
        squares = []
        while board != 0:
            square = board & -board
            squares.append(int(math.log2(square)))
            board = board ^ square
        return squares

    def mirror(self) -> 'BitBoard':
        return self.mirror_vertical().mirror_horizontal()

    def mirror_vertical(self) -> 'BitBoard':
        bitboard_array = np.array([self.board], dtype=np.uint64)
        return BitBoard(bitboard_array.byteswap().item(), self.board_type)

    def mirror_horizontal(self) -> 'BitBoard':
        # Convert the 64-bit integer to an array of 8 bytes
        bytes_array = np.array([self.board], dtype=np.uint64).view(np.uint8)
        # Reverse the bits in each byte using bitwise operations
        reversed_bytes = np.array([reverse_bits(byte) for byte in bytes_array],
                                  dtype=np.uint8)
        # Combine the reversed bytes back into a 64-bit integer
        mirrored_bitboard = reversed_bytes.view(np.uint64)[0]
        return BitBoard(int(mirrored_bitboard.item()), self.board_type)


def serialize_bit(bit: int) -> int:
    if bit == 0:
        raise ValueError("Cannot serialize bit: no bits are set.")
    if bit & (bit - 1) != 0:
        raise ValueError("Input must have only one bit set.")
    square = bit & -bit
    square = int(math.log2(square))
    return square


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
        prev_square = current_square
        if offset > 0:
            current_square = current_square << abs_offset
        else:
            current_square = current_square >> abs_offset
        if (not current_square == 0 and
                not prev_square == 0 and
                chebyshev_distance(serialize_bit(prev_square), serialize_bit(current_square)) > 1):
            break
        if current_square > 2 ** 63 or current_square == 0:
            break
        path |= current_square
        is_first_iteration = False
    return path


def get_file(square: int) -> int:
    return square % 8


def get_rank(square: int) -> int:
    return square // 8
