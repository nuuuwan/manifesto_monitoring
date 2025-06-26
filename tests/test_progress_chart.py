import os
import unittest

from mm import ProgressChart

TEST_PROGRESS_CHART = ProgressChart()


class TestCase(unittest.TestCase):

    def test_draw(self):
        TEST_PROGRESS_CHART.draw()
        self.assertTrue(os.path.exists(TEST_PROGRESS_CHART.CHART_PATH))
