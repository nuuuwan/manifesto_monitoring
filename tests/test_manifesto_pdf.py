import unittest

from mm import NPPManifestoPDF

TEST_MANIFESTO_PDF = NPPManifestoPDF()


class TestCase(unittest.TestCase):
    def test_raw_text(self):
        self.assertEqual(len(TEST_MANIFESTO_PDF.raw_text), 275852)

    def test_lines(self):
        lines = TEST_MANIFESTO_PDF.lines
        self.assertEqual(len(lines), 4_377)
