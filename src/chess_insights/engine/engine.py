from chess_insights.engine.move_generators import generate_all_moves
from chess_insights.game.chess_board import ChessBoard

import random


class Engine(ChessBoard):
    def __init__(self, board_state=None):
        super().__init__(board_state=board_state)

    def generate_move(self):
        candidate_moves = generate_all_moves(self.board_state)
        valid_moves = [(origin, target) for targets, _, origin in candidate_moves for target in
                       self._validate_moves(targets, _, origin)]
        return random.choice(valid_moves)
