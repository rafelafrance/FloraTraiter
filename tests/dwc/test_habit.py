import unittest

from tests.setup import to_ent

LABEL = "habit"


class TestHabit(unittest.TestCase):
    def test_habit_dwc_01(self):
        ent = to_ent(LABEL, "Stems often caespitose")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"habit": "cespitose"}}
        )
