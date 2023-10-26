import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "size"


class TestSize(unittest.TestCase):
    def test_shape_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Leaf ca. (12-)23-34 × 45-56 cm")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {
                    "leafSizeUncertain": "uncertain",
                    "leafLengthMinimumInCentimeters": 12.0,
                    "leafLengthLowInCentimeters": 23.0,
                    "leafLengthHighInCentimeters": 34.0,
                    "leafWidthLowInCentimeters": 45.0,
                    "leafWidthHighInCentimeters": 56.0,
                }
            },
        )
