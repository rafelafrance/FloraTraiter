import unittest

from tests.setup import to_dwc

LABEL = "habit"


class TestHabit(unittest.TestCase):
    def test_habit_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Stems often caespitose"),
            {"dwc:dynamicProperties": {"habit": "cespitose"}},
        )
