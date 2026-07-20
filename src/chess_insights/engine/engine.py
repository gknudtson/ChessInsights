from chess_insights.engine import bitboard
from chess_insights.game.board_state import BoardState
from chess_insights.game.chess_board import ChessBoard

import random

from chess_insights.util.fen import board_from_fen


class Engine(ChessBoard):
    def __init__(self, board_state=None):
        super().__init__(board_state=board_state)

    def generate_move(self):
        valid_moves = self.get_valid_moves()
        return random.choice(valid_moves)


    def __set_board_state(self, board_state: BoardState):
        self._board_state = board_state


    def perft(
            self,
            depth: int,
            board_state: BoardState
    ) -> int:
        self.__set_board_state(board_state)
        if depth == 0:
            return 1
        valid_moves = self.get_valid_moves()
        if depth == 1:
            return len(valid_moves)
        num_positions = 0
        for origin, target in valid_moves:
            self.__set_board_state(board_state)
            new_board_state = self._apply_move(origin, target)
            num_positions += self.perft(depth - 1, new_board_state)
        return num_positions

if __name__ == "__main__":
    engine = Engine()
    print(engine.perft(2, engine.board_state))