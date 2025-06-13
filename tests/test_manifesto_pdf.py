import unittest
from mm import NPPManifestoPDF

TEST_MANIFESTO_PDF = NPPManifestoPDF()


class TestCase(unittest.TestCase):
    def test_raw_text(self):
        self.assertEqual(len(TEST_MANIFESTO_PDF.raw_text), 275_868)

    def test_lines(self):
        lines = TEST_MANIFESTO_PDF.lines
        self.assertEqual(len(lines), 4_377)

    def test_l2_topics(self):
        l2_topics = TEST_MANIFESTO_PDF.l2_topics
        self.assertEqual(len(l2_topics), 39)
        first_topic = l2_topics[0]
        self.assertEqual(first_topic.l1_num, 1)
        self.assertEqual(first_topic.l2_num, 1)
        self.assertEqual(
            first_topic.title,
            'A civilized citizen - An advanced human resource',
        )
