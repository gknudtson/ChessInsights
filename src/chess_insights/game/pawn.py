from chess_insights.engine.bitboard import BitBoard
from chess_insights.game.board_state import BoardState
from chess_insights.util.enum_chess_piece_type import Color, ChessPieceType, ColorChessPiece
from chess_insights.util.enum_file_and_rank import Rank


def handle_pawn_movement(board_state: BoardState,
                         piece_type: ColorChessPiece,
                         origin_square: int,
                         target_square: int,
                         new_piece_locations: dict[ColorChessPiece, BitBoard]
                         ) -> (int, int):
    """Handles en passant, double moves, and resets the fifty-move counter for pawns."""
    if piece_type.piece_type != ChessPieceType.PAWN:
        return 0, board_state.fifty_move_rule + 1

    en_passant_square = handle_en_passant(origin_square, target_square, piece_type.color)
    pawn_promotion(target_square, new_piece_locations, piece_type.color)
    handle_en_passant_capture(board_state, target_square, piece_type.color, new_piece_locations)

    return en_passant_square, 0


def handle_en_passant(origin_square: int, target_square: int, color: Color) -> int:
    """Determines the en passant square if applicable."""
    if abs(origin_square - target_square) == 16:
        return 1 << (target_square - 8 if color == Color.WHITE else target_square + 8)
    return 0


def handle_en_passant_capture(board_state: BoardState,
                              target_square: int,
                              color: Color,
                              new_piece_locations: dict[ColorChessPiece, BitBoard]
                              ):
    """Handles en passant captures."""
    en_passant_target_square = board_state.en_passant_square.board.bit_length() - 1
    capturing_pawn_direction = -8 if color == Color.WHITE else 8
    en_passant_capture_square = en_passant_target_square + capturing_pawn_direction

    if target_square == en_passant_target_square:
        captured_pawn = color.opposite().get_color_piece_by_type(ChessPieceType.PAWN)
        if captured_pawn:
            new_piece_locations[captured_pawn].clear_bit(en_passant_capture_square)


def pawn_promotion(target_square: int,
                   piece_locations: dict[ColorChessPiece, BitBoard],
                   color: Color
                   ):
    if (color == Color.WHITE and 1 << target_square & Rank.Eight != 0 or
            color == Color.BLACK and 1 << target_square & Rank.One != 0):
        piece_locations[color.get_color_piece_by_type(ChessPieceType.PAWN)].clear_bit(
            target_square)
        piece_locations[color.get_color_piece_by_type(ChessPieceType.QUEEN)].set_bit(
            target_square)


def pawn_movement(color: Color,
                  square: int
                  ) -> (int, int):
    if color == Color.WHITE:
        return square + 8, square + 16
    elif color == Color.BLACK:
        return square - 8, square - 16


def is_pawn_starting_rank(origin_square: int,
                          color: Color
                          ) -> bool:
    if color == Color.WHITE:
        is_starting_rank = 8 <= origin_square <= 15
    elif color == Color.BLACK:
        is_starting_rank = 48 <= origin_square <= 55

    return is_starting_rank
