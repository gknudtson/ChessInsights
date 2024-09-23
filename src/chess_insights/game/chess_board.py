from dataclasses import replace
from enum import Enum
from types import MappingProxyType

from chess_insights.chess_pieces.chess_piece import ChessPiece
from chess_insights.engine.bitboard import BitBoard
from chess_insights.game.board_state import BoardState
from chess_insights.util.enum_chess_piece_type import ColorChessPiece, Color, \
    get_chess_piece_by_fen, ChessPieceType
from chess_insights.util.enum_ray_direction import Direction
from chess_insights.engine.move_generators import generate_moves
from chess_insights.util.fen import board_from_fen
from chess_insights.util.serializers import serialize_board


# TODO figure out what methods should be private
class ChessBoard:
    def __init__(self, fen: str = None):
        self._board_state = board_from_fen(fen) if fen else board_from_fen()

    @property
    def board_state(self) -> BoardState:
        return self._board_state

    # need to consider if king castled and move rook too, pawn promotion, check for win/draw condition, castling rights on rook movement
    # and make sure that i'm understanding castling rights properly
    def move_piece(self, origin_square: int, target_square: int) -> BoardState:
        legal_moves = self.get_moves(origin_square)
        if target_square in legal_moves:
            fifty_move = self._board_state.fifty_move_rule
            castling_rights = self._board_state.castling_rights
            piece_type = self.get_piece_on_square(origin_square)
            enemy_piece_type = self.get_piece_on_square(target_square)
            new_piece_locations = dict(self.board_state.piece_locations)
            new_piece_locations[piece_type].clear_bit(origin_square)
            new_piece_locations[piece_type].set_bit(target_square)
            if piece_type.piece_type == ChessPieceType.KING:
                if piece_type.color == Color.WHITE:
                    castling_rights &= 0b0011
                elif piece_type.color == Color.BLACK:
                    castling_rights &= 0b1100
            if piece_type.piece_type == ChessPieceType.ROOK:
                if piece_type.color == Color.WHITE:
                    castling_rights &= 0b0011
                elif piece_type.color == Color.BLACK:
                    castling_rights &= 0b1100
            if piece_type.piece_type == ChessPieceType.PAWN:
                fifty_move = 0
                if abs(origin_square - target_square) == 16:
                    en_passant_square = 1 << (origin_square + (target_square - origin_square))
                else:
                    en_passant_square = 0
            else:
                fifty_move += 1
                en_passant_square = 0
            if enemy_piece_type:
                new_piece_locations[enemy_piece_type].clear_bit(target_square)
                fifty_move = 0
            new_board_state = replace(
                self.board_state,
                piece_locations=MappingProxyType(new_piece_locations),
                is_whites_turn=not self.board_state.is_whites_turn,
                en_passant_square=BitBoard(en_passant_square),
                move_number=self.board_state.move_number + 1,
                fifty_move_rule=fifty_move,
                castling_rights=castling_rights,
            )
        return self.board_state
    def get_moves(self, square: int) -> list[int]:
        piece_type = self.get_piece_on_square(square)
        piece_board = BitBoard(1 << square, piece_type)
        moves = generate_moves(piece_board, MappingProxyType(self._board_state.piece_locations))
        return serialize_board(moves)

    def get_piece_locations(self, piece: ColorChessPiece) -> BitBoard:
        return self._board_state.piece_locations.get(piece, None)

    def get_castling_rights(self) -> int:
        return self._board_state.castling_rights

    def is_whites_turn(self) -> bool:
        return self._board_state.is_whites_turn

    def is_square_occupied(self, square: int) -> bool:
        return (self._board_state.piece_locations[ColorChessPiece.ALL_PIECES].board & (
                1 << square)) != 0

    def is_piece_on_square(self, piece: ColorChessPiece, square: int) -> bool:
        piece_locations = self.get_piece_locations(piece).board
        return (piece_locations & (1 << square)) != 0

    def get_piece_on_square(self, square: int) -> ColorChessPiece | None:
        for piece in ColorChessPiece:
            if (piece.piece_type != ChessPieceType.ANY
                    and (self._board_state.piece_locations[piece].board & (1 << square)) != 0):
                return piece
        return None

    def __get_pieces_by_color(self, color: Color) -> BitBoard:
        match color:
            case Color.WHITE:
                return self.get_piece_locations(ColorChessPiece.WHITE_PIECES).board
            case Color.BLACK:
                return self.get_piece_locations(ColorChessPiece.BLACK_PIECES).board
            case Color.ANY:
                return self.get_piece_locations(ColorChessPiece.ALL_PIECES)
            case _:
                raise ValueError(f"No opposite for color {color}")

    # TODO not being used atm
    # def is_piece_in_path(self, origin_square: int, target_square: int) -> bool:
    #     direction = Direction.from_squares(origin_square, target_square)
    #     path = ChessBoard.generate_path(origin_square, target_square, direction)
    #     return (path & self._board_state.piece_locations[ColorChessPiece.ALL_PIECES].board) != 0
    #
    # @staticmethod
    # def generate_path(origin_square: int, target_square: int, direction: Enum) -> int:
    #     path = 0
    #     step = direction.value[1]
    #     if step == 0:
    #         return path
    #     current = origin_square + step
    #     while current != target_square:
    #         path |= 1 << current
    #         current += step
    #     path |= 1 << current
    #     return path

    # TODO mutator methods
    # def add_piece(self, piece: ColorChessPiece, square: int):
    #     self._board_state.piece_locations[piece].set_bit(square)
    #     self.update_all_pieces()
    #
    # def remove_piece(self, piece: ColorChessPiece, square: int):
    #     self._board_state.piece_locations[piece].clear_bit(square)
    #     self.update_all_pieces()
    #
    # def remove_piece_by_square(self, square: int):
    #     piece = self.get_piece_on_square(square)
    #     if piece:
    #         self._board_state.piece_locations[piece].clear_bit(square)
    #         self.update_all_pieces()
    #
    # def update_all_pieces(self):
    #     self.update_pieces(ColorChessPiece.WHITE_PIECES)
    #     self.update_pieces(ColorChessPiece.BLACK_PIECES)
    #     self._board_state.piece_locations[ColorChessPiece.ALL_PIECES].set_board(
    #         self._board_state.piece_locations[ColorChessPiece.WHITE_PIECES].board |
    #         self._board_state.piece_locations[ColorChessPiece.BLACK_PIECES].board)
    #
    # def update_pieces(self, pieces_by_color: ColorChessPiece):
    #     board = 0
    #     if pieces_by_color == ColorChessPiece.BLACK_PIECES:
    #         piece_types = "black"
    #     else:
    #         piece_types = "white"
    #     for piece in ColorChessPiece:
    #         if piece.value[1] == piece_types:
    #             board |= self._board_state.piece_locations[piece].board
    #     self._board_state.piece_locations[pieces_by_color].set_board(board)
