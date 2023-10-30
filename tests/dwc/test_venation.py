import unittest

from tests.setup import to_ent

LABEL = "venation"


class TestVenation(unittest.TestCase):
    def test_venation_01(self):
        ent = to_ent(LABEL, "leaf subflabellate")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"leafVenation": "subflabellate"}}
        )
