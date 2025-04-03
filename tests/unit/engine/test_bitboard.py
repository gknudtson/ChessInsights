import unittest
from chess_insights.backend.core.engine.bitboard import BitBoard, reverse_bits
from chess_insights.backend.core.util.enum_chess_piece_type import ColorChessPiece


class TestBitBoard(unittest.TestCase):

    def setUp(self):
        # Initialize a BitBoard for testing (e.g., a white rook with no pieces on board)
        self.bitboard = BitBoard(0, ColorChessPiece.WHITE_ROOK)

    def test_initialization(self):
        # Test that board initializes correctly
        self.assertEqual(self.bitboard.board, 0)
        self.assertEqual(self.bitboard.board_type, ColorChessPiece.WHITE_ROOK)

    def test_set_board(self):
        # Test setting the entire board
        new_board = 0x1234567890ABCDEF
        self.bitboard.set_board(new_board)
        self.assertEqual(self.bitboard.board, new_board)

    def test_invalid_board_value(self):
        # Test setting an invalid board value (greater than 64 bits)
        with self.assertRaises(ValueError):
            self.bitboard.set_board(1 << 64)

    def test_set_bit(self):
        # Test setting individual bits
        self.bitboard.set_bit(0)  # Set bit at square 0
        self.assertEqual(self.bitboard.board, 1)
        self.bitboard.set_bit(63)  # Set bit at square 63
        self.assertEqual(self.bitboard.board, (1 | (1 << 63)))

    def test_set_bit_out_of_bounds(self):
        # Test setting bits out of bounds
        with self.assertRaises(ValueError):
            self.bitboard.set_bit(64)
        with self.assertRaises(ValueError):
            self.bitboard.set_bit(-1)

    def test_clear_bit(self):
        # Test clearing individual bits
        self.bitboard.set_bit(0)  # Set bit at square 0
        self.bitboard.set_bit(63)  # Set bit at square 63
        self.bitboard.clear_bit(0)  # Clear bit at square 0
        self.assertEqual(self.bitboard.board, 1 << 63)
        self.bitboard.clear_bit(63)  # Clear bit at square 63
        self.assertEqual(self.bitboard.board, 0)

    def test_clear_bit_out_of_bounds(self):
        # Test clearing bits out of bounds
        with self.assertRaises(ValueError):
            self.bitboard.clear_bit(64)
        with self.assertRaises(ValueError):
            self.bitboard.clear_bit(-1)

    def test_mirror_horizontal(self):
        # Test horizontal mirroring (reversing bits in each byte)
        # Example: 0xFF00000000000000 (row 8) should become 0x00000000000000FF (row 1)
        self.bitboard.set_board(0x8040201008040201)
        mirrored_board = self.bitboard.mirror_horizontal()
        self.assertEqual(mirrored_board.board, 0x102040810204080)

    def test_mirror(self):
        # Test vertical mirroring (flipping ranks)
        # Example: 0xFF00000000000000 (row 8) should become 0x00000000000000FF (row 1)
        self.bitboard.set_board(0x9050301)
        mirrored_board = self.bitboard.mirror()
        self.assertEqual(mirrored_board.board, 0x80c0a09000000000)

    def test_reverse_bits(self):
        # Test reverse_bits function on a single byte
        self.assertEqual(reverse_bits(0b10101010), 0b01010101)
        self.assertEqual(reverse_bits(0b11110000), 0b00001111)
        self.assertEqual(reverse_bits(0b00000001), 0b10000000)

    def test_invalid_board_initialization(self):
        # Test initializing with a negative or too large bitboard
        with self.assertRaises(ValueError):
            BitBoard(1 << 65)
        with self.assertRaises(ValueError):
            BitBoard(-(1 << 65))

    def test_serialize_board(self):
        assert BitBoard.serialize_board(BitBoard(72057594037928065, None)) == [0, 7, 56]


if __name__ == "__main__":
    unittest.main()
