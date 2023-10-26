import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "subpart"


class TestSubpart(unittest.TestCase):
    def test_subpart_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "male leaf teeth")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"maleLeafTeeth": "leaf teeth"}})

    def test_subpart_dwc_02(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Missing leaf teeth")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual, {"dynamicProperties": {"missingLeafTeeth": "missing leaf teeth"}}
        )
