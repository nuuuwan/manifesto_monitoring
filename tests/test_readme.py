import unittest

from mm import ReadMe


class TestCase(unittest.TestCase):
    def test_build(self):
        ReadMe().build()
