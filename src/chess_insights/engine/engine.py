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
        current_board_state = self.board_state
        num_positions = 0
        for move in valid_moves:
            origin, target = move
            self.__set_board_state(current_board_state)
            self.move_piece(origin, target)
            num_positions += self.perft(depth - 1, self.board_state)
        return num_positions

if __name__ == "__main__":
    engine = Engine()
    print(engine.perft(3, engine.board_state))