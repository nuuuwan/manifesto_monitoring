import unittest
from mm import NPPManifestoPDF
import json

TEST_MANIFESTO = NPPManifestoPDF().get_manifesto()


class TestCase(unittest.TestCase):
    def test_l1_topics(self):
        l1_topics = TEST_MANIFESTO.l1_topics
        self.assertEqual(len(l1_topics), 4)
        first_topic = l1_topics[0]
        self.assertEqual(first_topic.l1_num, 1)
        self.assertEqual(
            first_topic.title, 'A fulfilling life - A comfortable country'
        )

        first_l2_topic = first_topic.l2_topics[0]
        self.assertEqual(first_l2_topic.l1_num, 1)
        self.assertEqual(first_l2_topic.l2_num, 1)
        self.assertEqual(
            first_l2_topic.title,
            'A civilized citizen - An advanced human resource',
        )

    def test_to_dict(self):
        print(
            json.dumps(TEST_MANIFESTO.to_dict(), indent=2, ensure_ascii=False)
        )

    def test_to_dense_dict(self):
        print(
            json.dumps(
                TEST_MANIFESTO.to_dense_dict(), indent=2, ensure_ascii=False
            )
        )
