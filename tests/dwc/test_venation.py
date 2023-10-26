import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "venation"


class TestVenation(unittest.TestCase):
    def test_venation_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "leaf subflabellate")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual, {"dynamicProperties": {"leafVenation": "subflabellate"}}
        )
