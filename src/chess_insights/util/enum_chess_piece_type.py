from enum import Enum


class ChessPieceType(Enum):
    ANY = 'any'
    PAWN = 'pawn'
    KNIGHT = 'knight'
    BISHOP = 'bishop'
    ROOK = 'rook'
    QUEEN = 'queen'
    KING = 'king'
    # TODO possibly add methods to get colorpieces by type


class Color(Enum):
    ANY = 'any'
    WHITE = 'white'
    BLACK = 'black'

    def opposite(self):
        match self:
            case Color.WHITE:
                return Color.BLACK
            case Color.BLACK:
                return Color.WHITE
            case _:
                raise ValueError(f"No opposite for color {self}")

    def get_piece_group(self):
        match self:
            case Color.WHITE:
                return ColorChessPiece.WHITE_PIECES
            case Color.BLACK:
                return ColorChessPiece.BLACK_PIECES
            case Color.ANY:
                return ColorChessPiece.ALL_PIECES
            case _:
                raise TypeError(f"No general board for {self}")

    def get_color_piece_by_type(self, piece_type: ChessPieceType) -> "ColorChessPiece":
        """Retrieves the specific ColorChessPiece for the given color and type."""
        try:
            return next(piece for piece in ColorChessPiece if
                        piece.piece_type == piece_type and piece.color == self)
        except StopIteration:
            raise ValueError(f"No {piece_type.name} found for color {self.name}")


class ColorChessPiece(Enum):
    ALL_PIECES = (ChessPieceType.ANY, Color.ANY, '_')
    WHITE_PIECES = (ChessPieceType.ANY, Color.WHITE, '_')
    BLACK_PIECES = (ChessPieceType.ANY, Color.BLACK, '_')

    WHITE_PAWN = (ChessPieceType.PAWN, Color.WHITE, 'P')
    WHITE_KNIGHT = (ChessPieceType.KNIGHT, Color.WHITE, 'N')
    WHITE_BISHOP = (ChessPieceType.BISHOP, Color.WHITE, 'B')
    WHITE_ROOK = (ChessPieceType.ROOK, Color.WHITE, 'R')
    WHITE_QUEEN = (ChessPieceType.QUEEN, Color.WHITE, 'Q')
    WHITE_KING = (ChessPieceType.KING, Color.WHITE, 'K')

    BLACK_PAWN = (ChessPieceType.PAWN, Color.BLACK, 'p')
    BLACK_KNIGHT = (ChessPieceType.KNIGHT, Color.BLACK, 'n')
    BLACK_BISHOP = (ChessPieceType.BISHOP, Color.BLACK, 'b')
    BLACK_ROOK = (ChessPieceType.ROOK, Color.BLACK, 'r')
    BLACK_QUEEN = (ChessPieceType.QUEEN, Color.BLACK, 'q')
    BLACK_KING = (ChessPieceType.KING, Color.BLACK, 'k')

    @property
    def piece_type(self):
        return self.value[0]

    @property
    def color(self):
        return self.value[1]

    @property
    def fen(self):
        return self.value[2]


def get_chess_piece_by_fen(fen_char: str) -> ColorChessPiece:
    for piece in ColorChessPiece:
        if piece.fen == fen_char:
            return piece
    raise ValueError(f"No piece found for FEN character {fen_char}")


def get_pieces_by_color(color: Color) -> list[ColorChessPiece]:
    return [piece for piece in ColorChessPiece
            if piece.color == color and piece.piece_type != ChessPieceType.ANY]
