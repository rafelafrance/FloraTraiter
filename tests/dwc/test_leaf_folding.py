import unittest

from tests.setup import to_ent

LABEL = "leaf_folding"


class TestLeafFolding(unittest.TestCase):
    def test_leaf_folding_dwc_01(self):
        ent = to_ent(LABEL, "cucullate")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"leafFolding": "cucullate"}}
        )
