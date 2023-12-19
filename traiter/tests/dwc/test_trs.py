import unittest

from tests.setup import to_dwc

LABEL = "trs"


class TestTRS(unittest.TestCase):
    def test_trs_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "TRS: NE/14 NW1/4 NW1/4 Nw1/4 S21 T39S R20E"),
            {"dwc:dynamicProperties": {"TRSPresent": "present"}},
        )
