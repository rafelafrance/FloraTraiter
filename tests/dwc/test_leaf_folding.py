import unittest

from tests.setup import to_dwc

LABEL = "leaf_folding"


class TestLeafFolding(unittest.TestCase):
    def test_leaf_folding_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "cucullate"),
            {"dwc:dynamicProperties": {"leafFolding": "cucullate"}},
        )
