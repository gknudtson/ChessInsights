import math


def serialize_board(board: int) -> list[int]:
    squares = []
    while board != 0:
        square = board & -board
        squares.append(int(math.log2(square)))
        board = board ^ square
    return squares
