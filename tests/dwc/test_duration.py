import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "duration"


class TestDuration(unittest.TestCase):
    def test_duration_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "juvenile leaves persistent for a long period.")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"leafDuration": "persistent"}})
