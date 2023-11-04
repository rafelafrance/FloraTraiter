import unittest

from tests.setup import to_dwc

LABEL = "size"


class TestSize(unittest.TestCase):
    def test_size_dwc_01(self):
        self.maxDiff = None
        self.assertEqual(
            to_dwc(LABEL, "Leaf ca. (12-)23-34 × 45-56 cm"),
            {
                "dwc:dynamicProperties": {
                    "leafSize": (
                        "uncertain: True ~ "
                        "lengthMinimumInCentimeters: 12.0 ~ "
                        "lengthLowInCentimeters: 23.0 ~ "
                        "lengthHighInCentimeters: 34.0 ~ "
                        "widthLowInCentimeters: 45.0 ~ "
                        "widthHighInCentimeters: 56.0"
                    )
                }
            },
        )
