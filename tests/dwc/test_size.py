import unittest

from tests.setup import to_ent

LABEL = "size"


class TestSize(unittest.TestCase):
    def test_shape_dwc_01(self):
        ent = to_ent(LABEL, "Leaf ca. (12-)23-34 × 45-56 cm")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
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
