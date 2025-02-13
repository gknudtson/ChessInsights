import math

from chess_insights.engine.bitboard import BitBoard


def serialize_board(bit_board: BitBoard) -> list[int]:
    board = bit_board.board
    squares = []
    while board != 0:
        square = board & -board
        squares.append(int(math.log2(square)))
        board = board ^ square
    return squares
