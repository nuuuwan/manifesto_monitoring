import unittest

from mm import L2Chapter
from tests.test_manifesto_base import TEST_M


class TestCase(unittest.TestCase):

    def get_l2_chapter(self):
        l2_splits = TEST_M.l2_splits

        i_start, i_end = l2_splits[0]['i_line'] + 1, l2_splits[1]['i_line']
        chapter_lines = TEST_M.lines[i_start:i_end]
        return L2Chapter.from_lines(chapter_lines)

    def test_introduction_lines(self):
        l2_chapter = self.get_l2_chapter()
        introduction_lines = l2_chapter.introduction_lines

        self.assertEqual(
            introduction_lines[0],
            "Education is a cultural process that generates new knowledge by acquiring and",
        )
        self.assertEqual(
            introduction_lines[-1],
            "percentage of the gross domestic product up to 6%.",
        )
        self.assertEqual(len(introduction_lines), 27)

    def test_principles(self):
        l2_chapter = self.get_l2_chapter()
        self.assertEqual(len(l2_chapter.principles), 6)
        self.assertEqual(
            l2_chapter.principles,
            [
                'Free education and equal access',
                'Relevance to human development and employment',
                'Acceptability for all',
                'Responsible citizens accountable to society',
                'Sustainability and innovation',
                'Lifelong learning',
            ],
        )

    def test_activities(self):
        l2_chapter = self.get_l2_chapter()
        self.assertEqual(len(l2_chapter.activities), 17)
        self.assertEqual(
            l2_chapter.activities[0],
            "Early Childhood Development Education",
        )
        self.assertEqual(
            l2_chapter.activities[-1],
            "Distance Education",
        )
