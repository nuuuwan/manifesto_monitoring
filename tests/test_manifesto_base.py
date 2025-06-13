import unittest

from mm import NPPManifesto

TEST_M = NPPManifesto()


class TestCase(unittest.TestCase):
    def test_raw_text(self):
        raw_text = TEST_M.raw_text
        self.assertEqual(len(raw_text), 275_868)

    def test_lines(self):
        lines = TEST_M.lines
        self.assertEqual(len(lines), 43_77)

        for i, line in enumerate(lines[:300]):
            print(i, f'"{line}"')
