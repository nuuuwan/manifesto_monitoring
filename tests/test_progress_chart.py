import os
import unittest

from utils import Time, TimeFormat

from mm import ProgressChart

TEST_PROGRESS_CHART = ProgressChart()


class TestCase(unittest.TestCase):
    def test_method(self):
        d_list = TEST_PROGRESS_CHART.d_list
        last_d = d_list[-1]
        self.assertEqual(last_d["date"], TimeFormat.DATE.format(Time.now()))

    def test_draw(self):
        TEST_PROGRESS_CHART.draw()
        self.assertTrue(os.path.exists(TEST_PROGRESS_CHART.CHART_PATH))
