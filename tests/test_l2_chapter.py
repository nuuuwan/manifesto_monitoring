import unittest

from mm import L2Chapter
from tests.test_manifesto_base import TEST_M


class TestCase(unittest.TestCase):
    def test_method(self):
        l2_splits = TEST_M.l2_splits
        c1_l2 = l2_splits[0]
        c2_l2 = l2_splits[1]
        i_start = c1_l2['i_line']
        i_end = c2_l2['i_line']
        chapter_lines = TEST_M.lines[i_start:i_end]
        l2_chapter = L2Chapter.from_lines(chapter_lines)
        self.assertEqual(len(l2_chapter.introduction_lines), 3)
