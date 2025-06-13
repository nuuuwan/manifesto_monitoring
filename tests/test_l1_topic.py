import unittest
from mm import L1Topic


class TestCase(unittest.TestCase):
    def test_from_line(self):
        line = '1. Education'
        l1_topic = L1Topic.from_line(line)
        self.assertIsNotNone(l1_topic)
        self.assertEqual(l1_topic.l1_num, 1)
        self.assertEqual(l1_topic.title, 'Education')
        self.assertEqual(l1_topic.l2_topics, [])
