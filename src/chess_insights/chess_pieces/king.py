from chess_insights.engine.bitboard import BitBoard
from chess_insights.util.enum_chess_piece_type import Color


def get_castling_moves(color: Color, castling_rights: int, enemy_attacks_board: BitBoard,
                       collisions_board: BitBoard) -> BitBoard:
    if color == Color.WHITE:
        castling_rights &= 0b11
        enemy_attacks = enemy_attacks_board.board
        collisions = collisions_board.board
        return __get_castle_moves(castling_rights, enemy_attacks, collisions)

    elif color == Color.BLACK:
        castling_rights = castling_rights >> 2
        enemy_attacks = enemy_attacks_board.mirror_vertical().board
        collisions = collisions_board.mirror_vertical().board
        return __get_castle_moves(castling_rights, enemy_attacks, collisions).mirror_vertical()


def __get_castle_moves(castling_rights: int, enemy_attacks: int, collisions: int) -> BitBoard:
    moves = 0
    king_path_short = 112
    rook_path_short = 96
    king_path_long = 28
    rook_path_long = 14
    castling_rights &= 0b11

    castle_short = (enemy_attacks & king_path_short == 0 and castling_rights & 0b01 == 0b01
                    and collisions & rook_path_short == 0)
    castle_long = (enemy_attacks & king_path_long == 0 and castling_rights & 0b1 == 0b1
                   and collisions & rook_path_long == 0)
    if castle_short:
        moves |= 64
    if castle_long:
        moves |= 4

    return BitBoard(moves)

