from copy import deepcopy
from chess_insights.util.enum_chess_piece_type import ColorChessPiece
from chess_insights.engine.bitboard import BitBoard
from dataclasses import dataclass, replace
from types import MappingProxyType


@dataclass(frozen=True)
class BoardState:
    piece_locations: MappingProxyType[ColorChessPiece, BitBoard]
    is_whites_turn: bool
    en_passant_square: BitBoard
    fifty_move_rule: int
    move_number: int
    castling_rights: int

    def copy(self) -> "BoardState":
        """Manually create a copy of BoardState since MappingProxyType is immutable."""
        return replace(
            self,
            piece_locations=MappingProxyType({
                k: deepcopy(v) for k, v in self.piece_locations.items()
            })
        )
