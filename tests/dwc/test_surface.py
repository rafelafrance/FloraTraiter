import unittest

from tests.setup import to_ent

LABEL = "surface"


class TestSurface(unittest.TestCase):
    def test_surface_dwc_01(self):
        ent = to_ent(LABEL, "glabrous flowers")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"flowerSurface": "glabrous"}}
        )
