import json
import os
import unittest

from utils import File

from mm import NPPManifestoPDF

TEST_MANIFESTO = NPPManifestoPDF().get_manifesto()


class TestCase(unittest.TestCase):
    def test_l1_topics(self):
        l1_topics = TEST_MANIFESTO.l1_topics
        self.assertEqual(len(l1_topics), 4)
        first_topic = l1_topics[0]
        self.assertEqual(first_topic.l1_num, 1)
        self.assertEqual(
            first_topic.title, "A fulfilling life - A comfortable country"
        )

        first_l2_topic = first_topic.l2_topics[0]
        self.assertEqual(first_l2_topic.l1_num, 1)
        self.assertEqual(first_l2_topic.l2_num, 1)
        self.assertEqual(
            first_l2_topic.title,
            "A civilized citizen - An advanced human resource",
        )

    def test_to_dense_dict(self):
        s = json.dumps(
            TEST_MANIFESTO.to_dense_dict(), indent=2, ensure_ascii=False
        )
        self.assertEqual(len(s), 171041)

    def test_to_md_lines(self):
        md_path = os.path.join("data", "manifestos", "npp_manifesto.md")
        if os.path.exists(md_path):
            os.remove(md_path)
        md_lines = TEST_MANIFESTO.to_md_lines()
        File(md_path).write("\n\n".join(md_lines))
        self.assertTrue(os.path.exists(md_path))
