import unittest
from parameterized import parameterized
from chess_insights.chess_board import ChessBoard
from chess_insights.enum_ray_direction import Direction


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.white_pawns = self.chess_board.get_white_pawns()
        self.black_pawns = self.chess_board.get_black_pawns()

    def test_change_turn(self):
        self.chess_board.change_turn()
        assert not self.chess_board.is_whites_turn()

    def test_get_white_pawns_returns_int(self):
        self.assertIsInstance(self.chess_board.get_white_pawns(), int)

    def test_get_black_pawns_returns_int(self):
        self.assertIsInstance(self.chess_board.get_black_pawns(), int)

    def test_add_white_pawn(self):
        initial_white_pawns = self.white_pawns
        square = 10
        expected_result = initial_white_pawns | 2 ** square
        self.chess_board.add_white_pawn(square)
        updated_white_pawns = self.chess_board.get_white_pawns()
        self.assertEqual(updated_white_pawns, expected_result)

    def test_remove_white_pawn(self):
        initial_white_pawns = self.white_pawns
        square = 10
        expected_result = initial_white_pawns & ~(2 ** square)
        self.chess_board.remove_white_pawn(square)
        updated_white_pawns = self.chess_board.get_white_pawns()
        self.assertEqual(updated_white_pawns, expected_result)

    def test_add_black_pawn(self):
        initial_black_pawns = self.black_pawns
        square = 10
        expected_result = initial_black_pawns | 2 ** square
        self.chess_board.add_black_pawn(square)
        updated_black_pawns = self.chess_board.get_black_pawns()
        self.assertEqual(updated_black_pawns, expected_result)

    def test_remove_black_pawn(self):
        initial_black_pawns = self.black_pawns
        square = 10
        expected_result = initial_black_pawns & ~(2 ** square)
        self.chess_board.remove_black_pawn(square)
        updated_black_pawns = self.chess_board.get_black_pawns()
        self.assertEqual(updated_black_pawns, expected_result)

    def test_square_occupied(self):
        square = 10
        assert not self.chess_board.is_square_occupied(square)
        self.chess_board.add_white_pawn(square)
        assert self.chess_board.is_square_occupied(square)

    def test_is_white_piece_on_square(self):
        square = 10
        assert not self.chess_board.is_white_piece_on_square(square)
        self.chess_board.add_white_pawn(square)
        assert self.chess_board.is_white_piece_on_square(square)

    def test_is_black_piece_on_square(self):
        square = 10
        assert not self.chess_board.is_black_piece_on_square(square)
        self.chess_board.add_black_pawn(square)
        assert self.chess_board.is_black_piece_on_square(square)

    def test_remove_piece_from_square(self):
        square = 10
        self.chess_board.add_black_pawn(square)
        self.chess_board.remove_black_piece(square)
        assert not self.chess_board.is_square_occupied(square)
        self.chess_board.add_white_pawn(square)
        self.chess_board.remove_white_piece(square)
        assert not self.chess_board.is_square_occupied(square)

    @parameterized.expand([42, 2, 21, 16, 36, 32, 4, 0])
    def test_is_piece_in_path_no_pieces(self, target_square):
        origin_square = 18
        self.chess_board.add_white_pawn(origin_square)
        assert not self.chess_board.is_piece_in_path(origin_square, target_square)

    @parameterized.expand([42, 2, 21, 16, 36, 32, 4, 0])
    def test_is_piece_in_path_piece_in_path(self, target_square):
        origin_square = 18
        self.chess_board.add_white_pawn(target_square)
        assert self.chess_board.is_piece_in_path(origin_square, target_square)

    def test_generate_pawn_attacks_white(self):
        self.chess_board.add_white_pawn(8)
        self.chess_board.add_white_pawn(12)
        self.chess_board.add_white_pawn(15)
        assert self.chess_board.generate_pawn_attacks("white") == (
                2 ** 17 | 2 ** 19 | 2 ** 21 | 2 ** 22)

    def test_generate_pawn_attacks_black(self):
        self.chess_board.add_black_pawn(48)
        self.chess_board.add_black_pawn(52)
        self.chess_board.add_black_pawn(55)
        assert self.chess_board.generate_pawn_attacks("black") == (
                2 ** 41 | 2 ** 43 | 2 ** 45 | 2 ** 46)

    def test_generate_king_attacks_white_centered(self):
        self.chess_board.add_white_king(10)
        assert self.chess_board.generate_king_attacks("white") == (
                2 | 2 ** 2 | 2 ** 3 | 2 ** 9 | 2 ** 11 | 2 ** 17 | 2 ** 18 | 2 ** 19)

    def test_generate_king_attacks_white_corners(self):
        self.chess_board.add_white_king(0)
        self.chess_board.add_white_king(7)
        self.chess_board.add_white_king(56)
        self.chess_board.add_white_king(63)
        assert self.chess_board.generate_king_attacks("white") == (
                2 | 2 ** 6 | 2 ** 8 | 2 ** 9 | 2 ** 14 | 2 ** 15 | 2 ** 48 | 2 ** 49 | 2 ** 54 |
                2 ** 55 | 2 ** 57 | 2 ** 62)

    def test_generate_knight_attacks_white(self):
        self.chess_board.add_white_knight(20)
        assert self.chess_board.generate_knight_attacks("white") == (
                2 ** 3 | 2 ** 5 | 2 ** 10 | 2 ** 14 | 2 ** 26 | 2 ** 30 | 2 ** 35 | 2 ** 37)

    def test_generate_knight_attacks_white_corners(self):
        self.chess_board.add_white_knight(0)
        self.chess_board.add_white_knight(7)
        self.chess_board.add_white_knight(56)
        self.chess_board.add_white_knight(63)
        assert self.chess_board.generate_knight_attacks("white") == (
                2 ** 10 | 2 ** 13 | 2 ** 17 | 2 ** 22 | 2 ** 41 | 2 ** 46 | 2 ** 50 | 2 ** 53)

    def test_generate_bishop_attacks(self):
        self.chess_board.add_white_bishop(20)
        self.chess_board.add_white_bishop(19)
        assert self.chess_board.get_sliding_attacks("white", "bishop") == 36525115856403558

    def test_generate_bishop_attacks_with_collisions(self):
        self.chess_board.add_black_bishop(20)
        self.chess_board.add_black_bishop(19)
        self.chess_board.add_white_pawn(34)
        self.chess_board.add_black_pawn(11)
        self.chess_board.add_black_pawn(39)
        assert self.chess_board.get_sliding_attacks("black", "bishop") == 36241441856437346

    def test_get_file(self):
        assert self.chess_board.get_file(7) == 7

    def test_get_rank(self):
        assert self.chess_board.get_rank(7) == 0

    def test_generate_diagonal_path(self):
        assert self.chess_board.generate_diagonal_path_to_edge_of_board(0, 9) == 9241421688590303745

    def test_generate_mask(self):
        assert self.chess_board.generate_mask(27, Direction.NE) == 9241421688590303745

    def test_serialize_board(self):
        self.chess_board.add_white_knight(0)
        self.chess_board.add_white_knight(7)
        self.chess_board.add_white_knight(56)
        assert self.chess_board.serialize_board(72057594037928065) == [0, 7, 56]

    def test_mirror_vertical(self):
        assert self.chess_board.mirror_vertical(73165767551) == 18356848623779577856

    def test_generate_rook_attacks(self):
        self.chess_board.add_white_rook(28)
        self.chess_board.add_white_rook(0)
        assert self.chess_board.get_sliding_attacks("white", "rook") == 1229782941971845630

    def test_generate_rook_attacks_with_collisions(self):
        self.chess_board.add_black_rook(28)
        self.chess_board.add_black_rook(0)
        self.chess_board.add_white_pawn(1)
        self.chess_board.add_black_pawn(8)
        self.chess_board.add_black_pawn(4)
        self.chess_board.add_black_pawn(31)
        self.chess_board.add_white_pawn(25)
        self.chess_board.add_white_pawn(26)
        assert self.chess_board.get_sliding_attacks("black", "rook") == 1157442769100214546

    def test_generate_rook_attacks_with_collisions_v2(self):
        self.chess_board.add_black_rook(28)
        self.chess_board.add_black_rook(0)
        self.chess_board.add_white_pawn(1)
        self.chess_board.add_black_pawn(8)
        self.chess_board.add_black_pawn(4)
        self.chess_board.add_black_pawn(30)
        self.chess_board.add_white_pawn(25)
        self.chess_board.add_white_pawn(26)
        assert self.chess_board.get_sliding_attacks("black", "rook") == 1157442766952730898