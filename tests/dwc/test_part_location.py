import unittest

from tests.setup import to_dwc

LABEL = "part_location"


class TestPartLocation(unittest.TestCase):
    def test_part_location_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "adnate to petiole for 1-2 mm"),
            {
                "dwc:dynamicProperties": {
                    "partAsDistance": "adnate to petiole for 1 - 2 mm"
                }
            },
        )
