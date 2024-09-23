from chess_insights.util.enum_chess_piece_type import get_chess_piece_by_fen, ColorChessPiece
from chess_insights.engine.bitboard import BitBoard
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class BoardState:
    piece_locations: MappingProxyType[ColorChessPiece, BitBoard]
    is_whites_turn: bool
    en_passant_square: BitBoard
    fifty_move_rule: int
    move_number: int
    castling_rights: int
