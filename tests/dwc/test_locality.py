import unittest

from tests.setup import to_ent

LABEL = "locality"


class TestLocality(unittest.TestCase):
    def test_locality_dwc_01(self):
        verb = "5 miles North of Mason off Hwy 386."
        ent = to_ent(LABEL, verb)
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(dwc.to_dict(), {"verbatimLocality": verb})
