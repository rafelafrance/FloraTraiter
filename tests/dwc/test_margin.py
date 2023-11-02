import unittest

from tests.setup import to_dwc

LABEL = "margin"


class TestMargin(unittest.TestCase):
    def test_margin_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "leaf margin shallowly undulate-crenate"),
            {"dwc:dynamicProperties": {"leafMargin": "undulate-crenate"}},
        )
