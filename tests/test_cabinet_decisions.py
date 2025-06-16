import unittest

from mm import CabinetDecision


class TestCase(unittest.TestCase):
    def test_list_all(self):
        cabinet_decisions = CabinetDecision.list_all()
        self.assertGreater(len(cabinet_decisions), 9000)
