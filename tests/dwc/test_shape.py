import unittest

from tests.setup import to_ent

LABEL = "shape"


class TestShape(unittest.TestCase):
    def test_shape_dwc_01(self):
        ent = to_ent(LABEL, "leaf suborbiculate")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dynamicProperties": {"leafShape": "orbicular"}}
        )
