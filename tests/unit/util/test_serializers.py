import unittest

from chess_insights.util.serializers import *


class TestSerializers(unittest.TestCase):
    def test_serialize_board(self):
        assert serialize_board(BitBoard(72057594037928065, None)) == [0, 7, 56]
