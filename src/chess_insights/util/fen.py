from types import MappingProxyType

from chess_insights.engine.bitboard import BitBoard
from chess_insights.game.board_state import BoardState
from chess_insights.util.enum_chess_piece_type import ColorChessPiece, get_chess_piece_by_fen, \
    ChessPieceType
from chess_insights.util.enum_square import Square


def board_from_fen(
        fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> BoardState:
    try:
        position, turn, castling_rights, en_passant_square, fifty_move_rule, move_number = (
            fen.split(" ", 5))
    except ValueError:
        raise ValueError(f"{fen} is not a valid fen.")

    # Initialize the piece locations
    piece_locations = {
        piece: BitBoard(0, piece) for piece in ColorChessPiece
    }

    # Determine whose turn it is
    is_whites_turn = turn == 'w'

    # Castling rights
    castling_rights_int = fen_to_castling_rights(castling_rights)

    # En passant square (convert from string like 'e3' to bitboard index)
    en_passant_square_board = BitBoard()
    if en_passant_square != '-':
        en_passant_square_board.set_bit(Square[en_passant_square].value)

    current_square = 56
    for char in position:
        if char == '/':
            current_square -= 16
        elif char.isdigit():
            current_square += int(char)
        else:
            piece = get_chess_piece_by_fen(char)
            piece_locations[piece].set_bit(current_square)
            current_square += 1

    # Update the white pieces, black pieces, and all pieces bitboards
    all_white_pieces = sum(bitboard.board for piece, bitboard in piece_locations.items() if
                           piece.color == ColorChessPiece.WHITE_PIECES.color)
    all_black_pieces = sum(bitboard.board for piece, bitboard in piece_locations.items() if
                           piece.color == ColorChessPiece.BLACK_PIECES.color)

    piece_locations[ColorChessPiece.WHITE_PIECES] = BitBoard(all_white_pieces,
                                                             ColorChessPiece.WHITE_PIECES)
    piece_locations[ColorChessPiece.BLACK_PIECES] = BitBoard(all_black_pieces,
                                                             ColorChessPiece.BLACK_PIECES)
    piece_locations[ColorChessPiece.ALL_PIECES] = BitBoard(all_white_pieces | all_black_pieces,
                                                           ColorChessPiece.ALL_PIECES)

    # Return the board state
    return BoardState(
        piece_locations=MappingProxyType(piece_locations),
        is_whites_turn=is_whites_turn,
        en_passant_square=en_passant_square_board,
        fifty_move_rule=int(fifty_move_rule),
        move_number=int(move_number) if int(move_number) > 1 else 0,
        castling_rights=castling_rights_int
    )


def fen_from_board(board_state: BoardState) -> str:
    """
    Generate a FEN string from a BoardState object.
    """
    position = []

    for rank in range(8):
        empty_squares = 0
        for file in range(8):
            square_index = 56 - rank * 8 + file  # Top-left (a8) is 56, bottom-right (h1) is 0

            # Identify the piece at the current square
            piece = next(
                (color_piece.fen for color_piece, bitboard in board_state.piece_locations.items()
                 if color_piece.piece_type != ChessPieceType.ANY and bitboard.board & (1 << square_index)),
                None
            )

            if piece:
                # Add empty squares before a piece
                if empty_squares > 0:
                    position.append(str(empty_squares))
                    empty_squares = 0
                position.append(piece)
            else:
                empty_squares += 1

        # Add remaining empty squares at the end of the rank
        if empty_squares > 0:
            position.append(str(empty_squares))
        if rank < 7:
            position.append('/')

    # Turn (w/b)
    turn = 'w' if board_state.is_whites_turn else 'b'

    # Castling rights
    castling_rights = castling_rights_to_fen(board_state.castling_rights)

    # En passant square
    en_passant_square = '-'
    if board_state.en_passant_square.board:
        en_passant_square_index = board_state.en_passant_square.board.bit_length() - 1
        en_passant_square = Square(en_passant_square_index).name

    # Assemble the FEN string
    return f"{''.join(position)} {turn} {castling_rights} {en_passant_square} {board_state.fifty_move_rule} {board_state.move_number if board_state.move_number > 0 else 1}"



def fen_to_castling_rights(fen: str) -> int:
    castling_rights = 0
    if 'K' in fen:
        castling_rights |= 0b0001
    if 'Q' in fen:
        castling_rights |= 0b0010
    if 'k' in fen:
        castling_rights |= 0b1000
    if 'q' in fen:
        castling_rights |= 0b0100
    return castling_rights


def castling_rights_to_fen(castling_rights: int) -> str:
    fen_castling = []

    if castling_rights & 0b0100:
        fen_castling.append('K')
    if castling_rights & 0b1000:
        fen_castling.append('Q')
    if castling_rights & 0b0001:
        fen_castling.append('k')
    if castling_rights & 0b0010:
        fen_castling.append('q')

    # If no castling rights are available, return "-"
    return ''.join(fen_castling) if fen_castling else '-'
