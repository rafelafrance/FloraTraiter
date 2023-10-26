import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "locality"


class TestLocality(unittest.TestCase):
    def test_locality_dwc_01(self):
        dwc = DarwinCore()
        verb = "5 miles North of Mason off Hwy 386."
        ent = to_ent(LABEL, verb)
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"verbatimLocality": verb})
