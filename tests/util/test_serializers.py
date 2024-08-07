import unittest

from chess_insights.util.serializers import *


class TestSerializers(unittest.TestCase):
    def test_serialize_board(self):
        assert serialize_board(72057594037928065) == [0, 7, 56]
