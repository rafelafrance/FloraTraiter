import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "margin"


class TestMargin(unittest.TestCase):
    def test_margin_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "leaf margin shallowly undulate-crenate")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual, {"dynamicProperties": {"leafMargin": "undulate-crenate"}}
        )
