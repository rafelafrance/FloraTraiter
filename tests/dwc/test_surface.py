import unittest

from tests.setup import to_dwc

LABEL = "surface"


class TestSurface(unittest.TestCase):
    def test_surface_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "glabrous flowers"),
            {"dwc:dynamicProperties": {"flowerSurface": "glabrous"}},
        )
