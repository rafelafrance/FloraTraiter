import unittest

from tests.setup import to_dwc

LABEL = "utm"


class TestUTM(unittest.TestCase):
    def test_utm_dwc_01(self):
        verb = "UTM: 12s 359602E 3718689N"
        self.assertEqual(
            to_dwc(LABEL, verb),
            {"dwc:dynamicProperties": {"verbatimUTM": verb}},
        )
