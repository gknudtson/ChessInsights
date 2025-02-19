import unittest
from chess_insights.game.chess_board import ChessBoard
from chess_insights.util.enum_square import Square

class TestPGN(unittest.TestCase):
    def test_checkmate_pgn(self):
        board = ChessBoard("r1bqkbnr/8/8/1p1QN1pp/Ppp1PP1P/2N3p1/8/R1B1KB1R w KQkq - 0 16")
        board.move_piece(Square.d5.value, Square.f7.value)
        self.assertEqual(board.pgn, "16. Qf7# 1-0 ")



if __name__ == '__main__':
    unittest.main()
