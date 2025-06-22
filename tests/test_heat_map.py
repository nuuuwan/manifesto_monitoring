import os
import unittest

from mm import HeatMap

TEST_HEAT_MAP = HeatMap()


class TestCase(unittest.TestCase):
    def test_heat_map(self):
        self.assertEqual(TEST_HEAT_MAP.n_manifesto_items, 1345)
        self.assertEqual(TEST_HEAT_MAP.n_x, 49)
        self.assertEqual(TEST_HEAT_MAP.n_y, 28)
        self.assertGreaterEqual(
            TEST_HEAT_MAP.n_x * TEST_HEAT_MAP.n_y,
            TEST_HEAT_MAP.n_manifesto_items,
        )

    def test_draw_grid(self):
        if os.path.exists(HeatMap.CHART_PATH):
            os.remove(HeatMap.CHART_PATH)
        TEST_HEAT_MAP.draw()
        self.assertTrue(os.path.exists(HeatMap.CHART_PATH))
