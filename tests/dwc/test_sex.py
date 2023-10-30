import unittest

from tests.setup import to_ent

LABEL = "sex"


class TestSex(unittest.TestCase):
    def test_sex_dwc_01(self):
        ent = to_ent(LABEL, "(pistillate)")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(dwc.to_dict(), {"sex": "pistillate"})
