import unittest

from tests.setup import to_dwc

LABEL = "sex"


class TestSex(unittest.TestCase):
    def test_sex_dwc_01(self):
        self.assertEqual(to_dwc(LABEL, "(pistillate)"), {"dwc:sex": "pistillate"})
