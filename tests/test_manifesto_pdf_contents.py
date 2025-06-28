import unittest

from tests.test_manifesto_pdf import TEST_MANIFESTO_PDF


class TestCase(unittest.TestCase):
    def test_contents_lines(self):
        contents_lines = TEST_MANIFESTO_PDF.contents_lines

        self.assertEqual(
            contents_lines[0], "01. A fulfilling life - A comfortable country"
        )
        self.assertEqual(
            contents_lines[-1],
            "04.9 A Sri Lankan nation - The universal citizen 126",
        )
