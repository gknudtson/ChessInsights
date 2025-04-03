from chess_insights.backend.core.util.enum_chess_piece_type import ColorChessPiece, ChessPieceType, Color, \
    get_pieces_by_color
from chess_insights.backend.core.util.enum_file_and_rank import Rank, File
from chess_insights.backend.core.util.enum_ray_direction import Direction
from .bitboard import BitBoard, generate_mask
from chess_insights.backend.core.game.castling import get_castling_moves
from chess_insights.backend.core.game.pawn import is_pawn_starting_rank, pawn_movement
from ..game.board_state import BoardState


def generate_all_moves(board_state: BoardState) -> list[tuple[list[int], ColorChessPiece, int]]:
    """Generate all moves for a given BoardState based on turn."""

    # Determine which color is playing
    color = Color.WHITE if board_state.is_whites_turn else Color.BLACK

    # Generate all moves
    return [
        (BitBoard.serialize_board(generate_moves(BitBoard(1 << square, board.board_type), board_state)),
         board.board_type, square)
        for piece in get_pieces_by_color(color)
        for board in [board_state.piece_locations[piece]]
        for square in BitBoard.serialize_board(board)
    ]


def generate_moves(piece_board: BitBoard, board_state: BoardState) -> BitBoard:
    match piece_board.board_type.piece_type:
        case ChessPieceType.PAWN:
            return generate_pawn_moves(piece_board, board_state)
        case ChessPieceType.KING:
            return generate_king_moves(piece_board, board_state)
        case _:
            return generate_sliding_and_knight_moves(piece_board, board_state)


def generate_attacks(piece_board: BitBoard, collisions: BitBoard) -> BitBoard:
    if collisions.board_type != ColorChessPiece.ALL_PIECES:
        raise ValueError(
            f"Collisions board has type {collisions.board_type}, needs to be ALL_PIECES"
        )

    piece_type = piece_board.board_type.piece_type
    match piece_type:
        case ChessPieceType.PAWN:
            return generate_pawn_attacks(piece_board)
        case ChessPieceType.KNIGHT:
            return generate_knight_attacks(piece_board)
        case ChessPieceType.KING:
            return generate_king_attacks(piece_board)
        case ChessPieceType.BISHOP | ChessPieceType.ROOK | ChessPieceType.QUEEN:
            return get_sliding_attacks(collisions, piece_board)
        case _:
            raise ValueError(f"Incorrect piece type passed to move_generator, {piece_type}")


def generate_attacks_by_color(board_state: BoardState, color: Color) -> BitBoard:
    collisions = board_state.piece_locations[ColorChessPiece.ALL_PIECES]
    attacks = 0
    pieces = get_pieces_by_color(color)
    for piece in pieces:
        board = board_state.piece_locations[piece]
        attacks |= generate_attacks(board, collisions).board

    return BitBoard(attacks)


def generate_sliding_and_knight_moves(piece_board: BitBoard, board_state: BoardState, ) -> BitBoard:
    attack_board = generate_attacks(piece_board,
                                    board_state.piece_locations[ColorChessPiece.ALL_PIECES]).board
    color_pieces = board_state.piece_locations[piece_board.board_type.color.get_piece_group()].board
    moves = attack_board ^ (attack_board & color_pieces)

    return BitBoard(moves, piece_board.board_type)


def generate_pawn_moves(piece_board: BitBoard, board_state: BoardState) -> BitBoard:
    collisions = board_state.piece_locations[ColorChessPiece.ALL_PIECES]
    attack_board = generate_attacks(piece_board, collisions).board
    color = piece_board.board_type.color
    opposite_color = color.opposite()
    opposite_color_pieces = board_state.piece_locations[opposite_color.get_piece_group()]
    attack_board &= (opposite_color_pieces.board | board_state.en_passant_square.board)
    square = BitBoard.serialize_board(piece_board)[0]
    pawn_pushes = pawn_movement(color, square)
    single_push_board = BitBoard()
    double_push_board = BitBoard()
    if 0 <= pawn_pushes[0] <= 63:
        single_push_board.set_bit(pawn_pushes[0])
    if 0 <= pawn_pushes[1] <= 63:
        double_push_board.set_bit(pawn_pushes[1])

    pawn_moves = single_push_board.board ^ (collisions.board & single_push_board.board)

    if pawn_moves != 0 and is_pawn_starting_rank(square,
                                                 piece_board.board_type.color):
        pawn_moves |= double_push_board.board ^ (collisions.board & double_push_board.board)

    moves = attack_board | pawn_moves

    return BitBoard(moves, piece_board.board_type)


def generate_king_moves(piece_board: BitBoard, board_state: BoardState) -> BitBoard:
    color = piece_board.board_type.color
    collisions = board_state.piece_locations[ColorChessPiece.ALL_PIECES]
    color_pieces = board_state.piece_locations[color.get_piece_group()].board
    king_attacks = generate_attacks(piece_board, collisions).board
    enemy_attacks = generate_attacks_by_color(board_state, color.opposite())
    king_moves = king_attacks ^ ((enemy_attacks.board | color_pieces) & king_attacks)
    castling_rights = board_state.castling_rights
    castle_moves = get_castling_moves(color, castling_rights, enemy_attacks, collisions).board
    moves = king_moves | castle_moves

    return BitBoard(moves, piece_board.board_type)


def get_sliding_attacks(collisions: BitBoard, piece_board: BitBoard) -> BitBoard:
    squares = BitBoard.serialize_board(piece_board)
    directions = Direction.get_directions(piece_board.board_type)

    attacks = generate_sliding_attacks(collisions, squares, directions)
    return attacks


def generate_sliding_attacks(
        collisions: BitBoard,
        squares: list[int],
        directions: list[Direction]
) -> BitBoard:
    mirrored_collisions = collisions.mirror()
    attacks = 0
    for square in squares:
        bit_square = 1 << square
        mirrored_square = BitBoard(bit_square, None).mirror()
        for direction in directions:
            mask = generate_mask(square, direction)
            mirrored_mask = BitBoard(mask, None).mirror()
            positive_path = (collisions.board & mask) - 2 * bit_square
            negative_path = (BitBoard((
                    (mirrored_collisions.board & mirrored_mask.board) - 2 * mirrored_square.board),
                None)
                             .mirror())
            path = positive_path ^ negative_path.board
            attacks |= path & mask

    return BitBoard(attacks, None)


def generate_pawn_attacks(pawn_board: BitBoard) -> BitBoard:
    pawns = pawn_board.board
    a_file = File.A.value
    h_file = File.H.value

    if pawn_board.board_type.color == Color.WHITE:
        east_attacks = (pawns & ~h_file) << 9
        west_attacks = (pawns & ~a_file) << 7
    elif pawn_board.board_type.color == Color.BLACK:
        east_attacks = (pawns & ~h_file) >> 7
        west_attacks = (pawns & ~a_file) >> 9

    return BitBoard(east_attacks | west_attacks, None)


def generate_knight_attacks(knight_board: BitBoard) -> BitBoard:
    knights = knight_board.board
    a_file = File.A.value
    b_file = File.B.value
    g_file = File.G.value
    h_file = File.H.value
    rank_1 = Rank.One.value
    rank_2 = Rank.Two.value
    rank_7 = Rank.Seven.value
    rank_8 = Rank.Eight.value

    nne = (knights & ~(rank_7 | rank_8 | h_file)) << 17
    nee = (knights & ~(rank_8 | h_file | g_file)) << 10
    nnw = (knights & ~(rank_7 | rank_8 | a_file)) << 15
    nww = (knights & ~(rank_8 | a_file | b_file)) << 6
    sse = (knights & ~(rank_1 | rank_2 | h_file)) >> 15
    see = (knights & ~(rank_1 | g_file | h_file)) >> 6
    ssw = (knights & ~(rank_1 | rank_2 | a_file)) >> 17
    sww = (knights & ~(rank_1 | a_file | b_file)) >> 10
    attacks = nne | nee | nnw | nww | sse | see | ssw | sww

    return BitBoard(attacks, None)


def generate_king_attacks(king_board: BitBoard) -> BitBoard:
    king_square = king_board.board
    a_file = File.A.value
    h_file = File.H.value
    rank_1 = Rank.One.value
    rank_8 = Rank.Eight.value

    east = (king_square & ~h_file) << 1
    west = (king_square & ~a_file) >> 1
    north = (king_square & ~rank_8) << 8
    south = (king_square & ~rank_1) >> 8
    ne = (north & ~h_file) << 1
    nw = (north & ~a_file) >> 1
    se = (south & ~h_file) << 1
    sw = (south & ~a_file) >> 1
    attacks = east | west | north | south | ne | nw | se | sw

    return BitBoard(attacks, None)
