import unittest

from tests.setup import to_ent

LABEL = "subpart"


class TestSubpart(unittest.TestCase):
    def test_subpart_dwc_01(self):
        ent = to_ent(LABEL, "male leaf teeth")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"maleLeafTeeth": "leaf teeth"}}
        )

    def test_subpart_dwc_02(self):
        ent = to_ent(LABEL, "Missing leaf teeth")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {"dwc:dynamicProperties": {"missingLeafTeeth": "missing leaf teeth"}},
        )
