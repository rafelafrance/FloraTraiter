import unittest

from tests.setup import to_dwc

LABEL = "size"


class TestSize(unittest.TestCase):
    def test_size_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Leaf ca. (12-)23-34 × 45-56 cm"),
            {
                "dwc:dynamicProperties": {
                    "leafSizeUncertain": "uncertain",
                    "leafLengthMinimumInCentimeters": 12.0,
                    "leafLengthLowInCentimeters": 23.0,
                    "leafLengthHighInCentimeters": 34.0,
                    "leafWidthLowInCentimeters": 45.0,
                    "leafWidthHighInCentimeters": 56.0,
                }
            },
        )
