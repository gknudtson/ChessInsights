from chess_insights.util.enum_chess_piece_type import ColorChessPiece


def moves_to_dests(
    moves: list[tuple[list[int], ColorChessPiece, int]]
) -> dict[str, list[str]]:
    """
    Convert generate_all_moves() output into chessground's `dests` format:

        { "e2": ["e3", "e4"], "b1": ["a3", "c3"], ... }

    On the JS side, chessground wants a Map, so build it with:
        new Map(Object.entries(destsFromPython))
    """
    dests: dict[str, list[str]] = {}
    for destinations, _piece, from_square in moves:
        from_coord = square_to_coord(from_square)
        dests.setdefault(from_coord, []).extend(
            square_to_coord(dst) for dst in destinations
        )
    return dests

FILES = "abcdefgh"
def square_to_coord(square: int) -> str:
    """
    Convert a 0-63 square index to algebraic notation.
    Assumes square 0 = a1, incrementing by file then rank (a1..h1, a2..h2, ...).
    Adjust this mapping if your BitBoard uses a different square numbering.
    """
    file_idx = square % 8
    rank_idx = square // 8
    return f"{FILES[file_idx]}{rank_idx + 1}"