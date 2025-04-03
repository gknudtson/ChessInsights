from dataclasses import replace

from types import MappingProxyType

from chess_insights.backend.core.game.castling import handle_castling, \
    update_castling_rights
from chess_insights.backend.core.game.pawn import handle_pawn_movement
from chess_insights.backend.core.engine.bitboard import BitBoard
from chess_insights.backend.core.game.board_state import BoardState
from chess_insights.backend.core.util.enum_chess_piece_type import ColorChessPiece, Color, \
    ChessPieceType

from chess_insights.backend.core.engine.move_generators import generate_moves, generate_attacks_by_color, \
    generate_all_moves
from chess_insights.backend.core.util.enum_game_status import GameStatus
from chess_insights.backend.core.util.fen import board_from_fen
from chess_insights.backend.core.util.pgn import convert_move_pgn


class ChessBoard:
    def __init__(self, fen: str = None, board_state: BoardState = None, pgn: str = ""):
        if board_state:
            self._board_state = board_state
        else:
            self._board_state = board_from_fen(
                fen) if fen else board_from_fen()
        self.pgn = pgn

    @property
    def board_state(self) -> BoardState:
        return self._board_state

    def move_piece(self,
                   origin_square: int,
                   target_square: int
                   ) -> None:
        """Move a piece from origin_square to target_square, and update BoardState and PGN."""
        new_board_state = self._generate_move_board_state(origin_square, target_square)
        self.pgn = self.get_new_pgn(origin_square, target_square, new_board_state)
        self._board_state = new_board_state

    def _generate_move_board_state(self,
                                   origin_square: int,
                                   target_square: int
                                   ) -> BoardState:
        """Move a piece from origin_square to target_square, and return the resulting BoardState."""
        piece_type = self.get_piece_on_square(origin_square)
        self.__validate_move(origin_square, target_square, piece_type)

        # Copy the board state instead of manually copying dictionaries
        temp_board_state = self._board_state.copy()

        # Convert MappingProxyType to a regular dictionary for modification
        new_piece_locations = dict(temp_board_state.piece_locations)

        # Remove piece from original position and move to new position
        new_piece_locations[piece_type].clear_bit(origin_square)
        new_piece_locations[piece_type].set_bit(target_square)

        # Handle castling rights updates
        castling_rights = update_castling_rights(
            temp_board_state.castling_rights, piece_type, origin_square
        )

        # Handle castling move if applicable
        handle_castling(piece_type, origin_square, target_square, new_piece_locations)

        # Handle pawn movement and en passant
        en_passant_square, fifty_move = handle_pawn_movement(
            temp_board_state, piece_type, origin_square, target_square, new_piece_locations
        )

        # Handle captures
        enemy_piece_type = self.get_piece_on_square(target_square)
        if enemy_piece_type:
            fifty_move = 0
            castling_rights = self.__handle_capture(
                enemy_piece_type, target_square, castling_rights, new_piece_locations
            )

        # Update all pieces bitboards
        new_piece_locations = self.__update_all_pieces(new_piece_locations)

        # Create a new board state
        new_board_state = replace(
            temp_board_state,
            piece_locations=MappingProxyType(new_piece_locations),
            is_whites_turn=not temp_board_state.is_whites_turn,
            en_passant_square=BitBoard(en_passant_square),
            move_number=temp_board_state.move_number + 1 if
            temp_board_state.is_whites_turn else temp_board_state.move_number,
            fifty_move_rule=fifty_move,
            castling_rights=castling_rights,
        )
        return new_board_state

    def get_new_pgn(self, origin_square: int, target_square: int,
                    new_board_state: BoardState) -> str:
        piece_type = self.get_piece_on_square(origin_square)
        is_capture = bool(self.get_piece_on_square(target_square))
        is_check = self.__is_king_in_check(
            new_board_state, Color.WHITE if new_board_state.is_whites_turn else Color.BLACK)

        pgn_substring = convert_move_pgn(origin_square, target_square, new_board_state,
                                         is_check, piece_type, is_capture,
                                         self.check_game_status(new_board_state))
        is_fen_black_start = new_board_state.is_whites_turn and self.pgn == ""
        return f"{new_board_state.move_number}. — {pgn_substring}" if is_fen_black_start else self.pgn + pgn_substring

    def get_moves(self,
                  square: int
                  ) -> list[int]:
        """Get valid moves for the piece at the given square."""
        piece_type = self.get_piece_on_square(square)
        if not piece_type:
            return []

        piece_board = BitBoard(1 << square, piece_type)
        candidate_moves = BitBoard.serialize_board(generate_moves(piece_board, self._board_state))

        # Validate moves using a copied board state
        valid_moves = self._validate_moves(candidate_moves, piece_type, square)

        return valid_moves

    def get_piece_on_square(self,
                            square: int
                            ) -> ColorChessPiece | None:
        """Return ColorChessPieceType on square."""
        for piece in ColorChessPiece:
            if (piece.piece_type != ChessPieceType.ANY
                    and (self._board_state.piece_locations[piece].board & (1 << square)) != 0):
                return piece
        return None

    @staticmethod
    def check_game_status(board_state: BoardState
                          ) -> GameStatus:
        """Check if the game has ended and return the appropriate status."""
        board = ChessBoard(board_state=board_state)
        moves = generate_all_moves(board_state)
        valid_moves = [board._validate_moves(*move_tuple) for move_tuple in moves]
        color = Color.WHITE if board_state.is_whites_turn else Color.BLACK
        # Flatten the list so we can just check len
        all_moves = sum(valid_moves, [])
        if not all_moves and board.__is_king_in_check(board_state, color):
            return GameStatus.CHECKMATE
        if not all_moves:
            return GameStatus.STALEMATE
        if board_state.fifty_move_rule >= 50:
            return GameStatus.DRAW_50_MOVE

        return GameStatus.ONGOING

    def _validate_moves(self,
                        candidate_moves: list[int],
                        piece_type: ColorChessPiece,
                        square: int
                        ) -> list[int]:
        """Filter out moves that would leave the king in check."""
        valid_moves = []

        for move in candidate_moves:
            temp_board_state = self._board_state.copy()

            # Copy the piece locations separately for modifications
            new_piece_locations = dict(temp_board_state.piece_locations)

            # Simulate the move
            enemy_piece_type = self.get_piece_on_square(
                move)
            if enemy_piece_type:
                new_piece_locations[enemy_piece_type].clear_bit(move)  # Remove captured piece

            new_piece_locations[piece_type].clear_bit(square)  # Remove moving piece
            new_piece_locations[piece_type].set_bit(move)  # Move piece to new square
            new_piece_locations = self.__update_all_pieces(new_piece_locations)
            simulated_board = replace(
                temp_board_state,
                piece_locations=MappingProxyType(new_piece_locations),

                is_whites_turn=not temp_board_state.is_whites_turn
            )

            # Validate that the move does not put the king in check
            if not self.__is_king_in_check(simulated_board, piece_type.color):
                valid_moves.append(move)

        return valid_moves

    def __validate_move(self,
                        origin_square: int,
                        target_square: int,
                        piece_type: ColorChessPiece
                        ):
        """Ensure that is proper turn and that target square is a valid move."""
        if (piece_type.color == Color.WHITE) ^ self._board_state.is_whites_turn:
            raise ValueError(
                f"Invalid move: {piece_type.color} piece attempted to move on opponent's turn.")
        if target_square not in self.get_moves(origin_square):
            raise ValueError(
                f"Invalid move: {piece_type} cannot move from {origin_square} to {target_square}.")

    @staticmethod
    def __is_king_in_check(board_state: BoardState,
                           color: Color
                           ) -> bool:
        """Return True if the color King is in check in board_state."""
        king_square = board_state.piece_locations[
            color.get_color_piece_by_type(ChessPieceType.KING)].board
        attacks_by_opponent = generate_attacks_by_color(board_state,
                                                        color.opposite()).board
        return bool(attacks_by_opponent & king_square)

    @staticmethod
    def __handle_capture(enemy_piece_type: ColorChessPiece,
                         target_square: int,
                         castling_rights: int,
                         new_piece_locations: dict[ColorChessPiece, BitBoard]
                         ):
        """Capture piece on target square and update castling rights if necessary."""
        # Update castling rights if capturing a rook
        castling_rights = update_castling_rights(castling_rights, enemy_piece_type, target_square) \
            if enemy_piece_type.piece_type == ChessPieceType.ROOK else castling_rights

        # Remove the captured piece
        new_piece_locations[enemy_piece_type].clear_bit(target_square)

        return castling_rights

    @staticmethod
    def __update_all_pieces(boards: dict[ColorChessPiece, BitBoard]
                            ) -> dict[ColorChessPiece, BitBoard]:
        """Update the bitboards for all pieces (WHITE_PIECES, BLACK_PIECES, ALL_PIECES)."""
        updated_boards = boards.copy()
        updated_boards[ColorChessPiece.WHITE_PIECES] = ChessBoard.__update_pieces(
            ColorChessPiece.WHITE_PIECES, boards)
        updated_boards[ColorChessPiece.BLACK_PIECES] = ChessBoard.__update_pieces(
            ColorChessPiece.BLACK_PIECES, boards)
        updated_boards[ColorChessPiece.ALL_PIECES] = BitBoard((
                updated_boards[ColorChessPiece.WHITE_PIECES].board | updated_boards[
            ColorChessPiece.BLACK_PIECES].board
        ), ColorChessPiece.ALL_PIECES)
        return updated_boards

    @staticmethod
    def __update_pieces(pieces_by_color: ColorChessPiece,
                        boards: dict[ColorChessPiece, BitBoard]
                        ) -> BitBoard:
        """Computes the bitboard for all pieces of a given color."""
        board = 0
        for piece in ColorChessPiece:
            if piece.value[1] == pieces_by_color.color and piece.value[0] != ChessPieceType.ANY:
                board |= boards[piece].board

        return BitBoard(board, pieces_by_color)
