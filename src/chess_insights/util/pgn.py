from chess_insights.game.board_state import BoardState
from chess_insights.util.enum_game_status import GameStatus
from .enum_chess_piece_type import ChessPieceType, Color, ColorChessPiece
from .enum_square import Square, chebyshev_distance


def convert_move_pgn(origin_square: int,
                     target_square: int,
                     new_board_state: BoardState,
                     is_check: bool,
                     piece: ColorChessPiece,
                     is_capture: bool,
                     status: GameStatus,
                     ) -> str:
    pgn = f"{new_board_state.move_number}. " if not new_board_state.is_whites_turn else " "
    if piece.piece_type == ChessPieceType.KING and chebyshev_distance(origin_square,
                                                                      target_square) == 2:
        pgn += "0-0" if Square(target_square).name.startswith('g') else "0-0-0"
    else:
        move_notation = f"{piece.fen.capitalize() if piece.fen.capitalize() != 'P' else ''}{'x' if is_capture else ''}{Square(target_square).name}"
        if piece.piece_type == ChessPieceType.PAWN and is_capture:
            move_notation = f"{Square(origin_square).name[0]}x{Square(target_square).name}"
        pgn += move_notation

    if status in {GameStatus.DRAW_50_MOVE, GameStatus.STALEMATE, GameStatus.DRAW_REPETITION,
                  GameStatus.DRAW_INSUFFICIENT_MATERIAL}:
        pgn += " 1/2-1/2"
    elif status == GameStatus.CHECKMATE:
        pgn += "# 1-0" if piece.color == Color.WHITE else "# 0-1"
    elif is_check:
        pgn += "+"

    return pgn + " "
