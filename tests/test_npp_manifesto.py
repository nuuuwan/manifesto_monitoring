import json
import unittest

from mm import NPPManifesto

TEST_M = NPPManifesto()


class TestCase(unittest.TestCase):
    def test_raw_text(self):
        raw_text = TEST_M.raw_text
        self.assertEqual(len(raw_text), 275_868)

    def test_lines(self):
        lines = TEST_M.lines
        self.assertEqual(len(lines), 4_363)

        for i, line in enumerate(lines[:300]):
            print(i, f'"{line}"')

    def test_l1_list(self):
        l1_list = TEST_M.l1_list
        self.assertEqual(len(l1_list), 4)
        self.assertEqual(
            l1_list,
            [
                {
                    'l1_num': 1,
                    'title': 'A fulfilling life - A comfortable country',
                },
                {
                    'l1_num': 2,
                    'title': 'An honourable life - A safer country',
                },
                {'l1_num': 3, 'title': 'A modern life - A wealthy nation'},
                {
                    'l1_num': 4,
                    'title': 'A dignified life - A strong country',
                },
            ],
        )

    def test_l2_list(self):
        l2_list = TEST_M.l2_list
        self.assertEqual(len(l2_list), 39)
        self.assertEqual(
            l2_list[0],
            {
                'l1_num': 1,
                'l2_num': 1,
                'title': 'A civilized citizen - An advanced human resource',
                'page_num': 9,
            },
        )

    def test_manifesto(self):
        manifesto = TEST_M.manifesto
        self.assertEqual(len(manifesto), 4)
        print(json.dumps(manifesto, indent=2, ensure_ascii=False))
