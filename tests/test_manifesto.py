import unittest
from mm import NPPManifestoPDF

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
        self.assertEqual(first_topic.l2_topics, [])
