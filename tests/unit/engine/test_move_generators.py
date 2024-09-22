import unittest
from parameterized import parameterized

from chess_insights.engine.move_generators import *
from chess_insights.util.fen import board_from_fen


class TestMoveGenerators(unittest.TestCase):
    def test_generate_rook_attacks(self):
        self.assertEqual(
            get_sliding_attacks(BitBoard(268435457, ColorChessPiece.ALL_PIECES),
                                BitBoard(268435457, ColorChessPiece.WHITE_ROOK)).board,
            1229782941971845630
        )

    def test_generate_rook_attacks_with_collisions(self):
        self.assertEqual(
            get_sliding_attacks(BitBoard(2516582675, ColorChessPiece.ALL_PIECES),
                                BitBoard(268435457, ColorChessPiece.WHITE_ROOK)).board,
            1157442769100214546
        )

    def test_generate_rook_attacks_with_collisions_v2(self):
        self.assertEqual(
            get_sliding_attacks(BitBoard(1442840851, ColorChessPiece.ALL_PIECES),
                                BitBoard(268435457, ColorChessPiece.WHITE_ROOK)).board,
            1157442766952730898
        )

    def test_generate_queen_attacks(self):
        self.assertEqual(
            get_sliding_attacks(BitBoard(268435456, ColorChessPiece.ALL_PIECES),
                                BitBoard(268435456, ColorChessPiece.WHITE_QUEEN)).board,
            1266167048752878738
        )

    def test_generate_queen_attacks_two_queens(self):
        self.assertEqual(
            get_sliding_attacks(BitBoard(268435457, ColorChessPiece.ALL_PIECES),
                                BitBoard(268435457, ColorChessPiece.WHITE_QUEEN)).board,
            10507871247272859646
        )

    def test_generate_queen_attacks_with_collisions(self):
        self.assertEqual(
            get_sliding_attacks(BitBoard(9259475670827270547, ColorChessPiece.ALL_PIECES),
                                BitBoard(9223372037123211265, ColorChessPiece.WHITE_QUEEN)).board,
            9205467831842132882
        )

    def test_generate_pawn_attacks_white(self):
        self.assertEqual(
            generate_pawn_attacks(BitBoard(37120, ColorChessPiece.WHITE_PAWN)).board,
            6946816
        )

    def test_generate_pawn_attacks_black(self):
        self.assertEqual(
            generate_pawn_attacks(BitBoard(40813871623045120, ColorChessPiece.BLACK_PAWN)).board,
            116548232544256
        )

    def test_generate_king_attacks_white_centered(self):
        self.assertEqual(
            generate_king_attacks(BitBoard(1024, ColorChessPiece.WHITE_KING)).board,
            920078
        )

    def test_generate_king_attacks_white_corners(self):
        self.assertEqual(
            generate_king_attacks(BitBoard(9295429630892703873, ColorChessPiece.WHITE_KING)).board,
            4810688826961871682
        )

    def test_generate_knight_attacks_white(self):
        self.assertEqual(
            generate_knight_attacks(BitBoard(1048576, ColorChessPiece.WHITE_KNIGHT)).board,
            172939559976
        )

    def test_generate_knight_attacks_white_corners(self):
        self.assertEqual(
            generate_knight_attacks(
                BitBoard(9295429630892703873, ColorChessPiece.WHITE_KNIGHT)).board,
            10205666933351424
        )

    def test_generate_bishop_attacks(self):
        self.assertEqual(
            get_sliding_attacks(BitBoard(1572864, ColorChessPiece.ALL_PIECES),
                                BitBoard(1572864, ColorChessPiece.WHITE_BISHOP)).board,
            36525115856403558
        )

    def test_generate_bishop_attacks_with_collisions(self):
        self.assertEqual(
            get_sliding_attacks(BitBoard(566937257984, ColorChessPiece.ALL_PIECES),
                                BitBoard(1572864, ColorChessPiece.WHITE_BISHOP)).board,
            36241441856437346
        )

    @parameterized.expand([
        (BitBoard(40813871623045120, ColorChessPiece.BLACK_PAWN), 116548232544256),
        (BitBoard(9295429630892703873, ColorChessPiece.BLACK_KNIGHT), 10205666933351424),
        (BitBoard(268435457, ColorChessPiece.WHITE_ROOK), 1229782941971845630),
    ])
    def test_generate_attacks(self, piece_board, expected_attacks):
        collisions = BitBoard(piece_board.board, ColorChessPiece.ALL_PIECES)
        attacks = generate_attacks(piece_board, collisions)
        self.assertEqual(attacks.board, expected_attacks)

    @parameterized.expand([[ColorChessPiece.BLACK_KNIGHT, 181419418583040],
                           [ColorChessPiece.WHITE_QUEEN, 2261181249756160]])
    def test_generate_sliding_and_knight_moves(self, piece_type, expected):
        board_state = board_from_fen("rnbqkbnr/pppppppp/8/8/8/8/8/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(generate_moves(board_state.piece_locations[piece_type], board_state).board,
                         expected)

    @parameterized.expand([[BitBoard(8796093022208, ColorChessPiece.WHITE_PAWN), 5629499534213120],
                           [BitBoard(2251799813685248, ColorChessPiece.BLACK_PAWN), 8830452760576],
                           [BitBoard(2048, ColorChessPiece.BLACK_PAWN), 20],
                           [BitBoard(65536, ColorChessPiece.WHITE_PAWN), 16777216]])
    def test_generate_pawn_moves(self, pawn_board, expected):
        board_state = board_from_fen()
        self.assertEqual(generate_moves(pawn_board, board_state).board, expected)

    def test_generate_pawn_moves_en_passant(self):
        board_state = board_from_fen(
            "rnbqkb1r/ppppp1pp/7n/4Pp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3"
        )
        pawn_board = BitBoard(2 ** 36, ColorChessPiece.WHITE_PAWN)
        self.assertEqual(generate_moves(pawn_board, board_state).board, 52776558133248)

    @parameterized.expand([[ColorChessPiece.WHITE_KING,
                            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 0],
                           [ColorChessPiece.BLACK_KING,
                            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 0],
                           [ColorChessPiece.BLACK_KING,
                            "r3k2r/8/8/8/8/8/8/3R4 w kq - 0 1", 6931039826523193344],
                           [ColorChessPiece.BLACK_KING,
                            "r3k2r/4R3/8/8/8/8/8/8 w kq - 0 1", 2886807361144487936],
                           [ColorChessPiece.WHITE_KING,
                            "rnbqkbnr/pppppppp/8/8/8/8/8/RNBQKBNR w KQkq - 0 1", 14336],
                           [ColorChessPiece.WHITE_KING, "8/8/8/8/8/8/8/R3K2R w KQ - 0 1", 14444],
                           [ColorChessPiece.WHITE_KING, "3r4/8/8/8/8/8/8/R3K2R w KQ - 0 1", 12384],
                           [ColorChessPiece.WHITE_KING, "4r3/8/8/8/8/8/8/R3K2R w KQ - 0 1", 10280],
                           [ColorChessPiece.WHITE_KING, "6r1/8/8/8/8/8/8/R3K2R w KQ - 0 1", 14380]])
    def test_generate_king_moves(self, king_type, fen, expected):
        board_state = board_from_fen(fen)
        self.assertEqual(generate_moves(board_state.piece_locations[king_type], board_state).board,
                         expected)


if __name__ == '__main__':
    unittest.main()
