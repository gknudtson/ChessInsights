from chess_insights.engine.bitboard import BitBoard
from chess_insights.util.enum_chess_piece_type import Color, ColorChessPiece, ChessPieceType
from chess_insights.util.enum_square import Square, chebyshev_distance


def update_castling_rights(castling_rights: int,
                           piece_type: ColorChessPiece,
                           square: int
                           ) -> int:
    """Update castling rights when the king or rook moves."""

    if piece_type.piece_type == ChessPieceType.KING:
        return castling_rights & (0b1100 if piece_type.color == Color.WHITE else 0b0011)

    if piece_type.piece_type == ChessPieceType.ROOK:
        rook_castling_map = {
            Square['a1'].value: 0b1101,  # White queenside
            Square['h1'].value: 0b1110,  # White kingside
            Square['a8'].value: 0b0111,  # Black queenside
            Square['h8'].value: 0b1011  # Black kingside
        }
        return castling_rights & rook_castling_map.get(square, castling_rights)

    return castling_rights


def handle_castling(piece_type: ColorChessPiece,
                    origin_square: int,
                    target_square: int,
                    new_piece_locations: dict
                    ) -> None:
    """Move the rook when castling."""
    if piece_type.piece_type == ChessPieceType.KING and chebyshev_distance(origin_square,
                                                                           target_square) > 1:
        rook, rook_target, rook_origin = get_castling_rook_squares(target_square)
        new_piece_locations[rook].set_bit(rook_target)
        new_piece_locations[rook].clear_bit(rook_origin)


def get_castling_rook_squares(target_square: int
                              ) -> tuple[ColorChessPiece, int, int]:
    """Return the rook involved in castling and its new and original positions."""

    rook = ColorChessPiece.BLACK_ROOK if target_square > 6 else ColorChessPiece.WHITE_ROOK

    # Default to queenside castling
    rook_target = target_square + 1
    rook_origin = target_square - 2

    # If kingside castling (target squares 6 or 62), override
    if target_square in (6, 62):
        rook_origin = target_square + 1
        rook_target = target_square - 1

    return rook, rook_target, rook_origin


def get_castling_moves(color: Color,
                       castling_rights: int,
                       enemy_attacks_board: BitBoard,
                       collisions_board: BitBoard
                       ) -> BitBoard:
    """Generate legal castling moves based on board state and castling rights."""

    if color == Color.WHITE:
        castling_rights &= 0b0011
        enemy_attacks = enemy_attacks_board.board
        collisions = collisions_board.board
        return __get_castle_moves(castling_rights, enemy_attacks, collisions)

    elif color == Color.BLACK:
        castling_rights = castling_rights >> 2
        enemy_attacks = enemy_attacks_board.mirror_vertical().board
        collisions = collisions_board.mirror_vertical().board
        return __get_castle_moves(castling_rights, enemy_attacks, collisions).mirror_vertical()


def __get_castle_moves(castling_rights: int,
                       enemy_attacks: int,
                       collisions: int
                       ) -> BitBoard:
    """Determine if castling is legal based on attack squares and piece positions."""

    moves = 0
    king_path_short = 112  # Kingside castling path
    rook_path_short = 96  # Kingside rook path
    king_path_long = 28  # Queenside castling path
    rook_path_long = 14  # Queenside rook path
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
