import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "shape"


class TestShape(unittest.TestCase):
    def test_shape_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "leaf suborbiculate")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"leafShape": "orbicular"}})
