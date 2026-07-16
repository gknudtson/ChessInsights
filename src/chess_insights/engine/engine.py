from chess_insights.game.chess_board import ChessBoard

import random


class Engine(ChessBoard):
    def __init__(self, board_state=None):
        super().__init__(board_state=board_state)

    def generate_move(self):
        valid_moves = self.get_valid_moves()
        return random.choice(valid_moves)
