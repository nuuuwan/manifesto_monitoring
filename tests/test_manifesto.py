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
        self.assertGreater(len(s), 100000)

    def test_to_md_lines(self):
        md_path = os.path.join("data", "manifestos", "npp_manifesto.md")
        if os.path.exists(md_path):
            os.remove(md_path)
        md_lines = TEST_MANIFESTO.to_md_lines()
        File(md_path).write("\n\n".join(md_lines))
        self.assertTrue(os.path.exists(md_path))

    def test_activities_per_l2_topic(self):

        for l2_topic in TEST_MANIFESTO.l2_topics:
            n_activities = l2_topic.n_activities
            self.assertTrue(
                1 <= n_activities <= 20,
                f"[{l2_topic.key}] {n_activities=} (Expected 1-20)",
            )

    def test_principles_per_l2_topic(self):
        for l2_topic in TEST_MANIFESTO.l2_topics:
            n_principles = l2_topic.n_principles
            # HACK - exceptions. These have no principles.
            if l2_topic.key in ["2.06", "4.01", "4.06"]:
                continue
            self.assertTrue(
                2 <= n_principles <= 10,
                f"[{l2_topic.key}] {n_principles=} (Expected 2-10)",
            )

    def test_items_per_activity(self):
        for activity in TEST_MANIFESTO.activity_list:
            n_items = activity.n_items
            self.assertTrue(
                1 <= n_items <= 32,
                f"[{activity.key}] {n_items=} (Expected 1-10)",
            )
