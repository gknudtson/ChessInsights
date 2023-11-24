from chess_insights.locations import Locations


class ChessBoard:
    locations = None

    def __init__(self):
        if ChessBoard.locations is None:
            raise ValueError("Locations is not set. Call set_locations to set it.")

    @classmethod
    def set_chess_board(cls, locations: Locations):
        cls.locations = locations

    def add_white_pawn(self, square: int):
        self.locations.white_pawns = self.locations.white_pawns | 1 << square

    def remove_white_pawn(self, square):
        self.locations.white_pawns = self.locations.white_pawns & ~(1 << square)
