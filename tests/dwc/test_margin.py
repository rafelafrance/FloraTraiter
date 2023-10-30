import unittest

from tests.setup import to_ent

LABEL = "margin"


class TestMargin(unittest.TestCase):
    def test_margin_dwc_01(self):
        ent = to_ent(LABEL, "leaf margin shallowly undulate-crenate")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dynamicProperties": {"leafMargin": "undulate-crenate"}}
        )
