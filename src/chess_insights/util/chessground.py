from collections import defaultdict

def moves_to_dests(
    moves: list[tuple[int, int]]
) -> dict[str, list[str]]:
    dests: dict[str, list[str]] = defaultdict(list)
    """
    Convert get_valid_moves() output into chessground's `dests` format:

        { "e2": ["e3", "e4"], "b1": ["a3", "c3"], ... }

    On the JS side, chessground wants a Map, so build it with:
        new Map(Object.entries(destsFromPython))
    """
    for origin, target in moves:
        dests[square_to_coord(origin)].append(square_to_coord(target))

    return dict(dests)

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