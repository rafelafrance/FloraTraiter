import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "habit"


class TestHabit(unittest.TestCase):
    def test_habit_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Stems often caespitose")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"habit": "cespitose"}})
