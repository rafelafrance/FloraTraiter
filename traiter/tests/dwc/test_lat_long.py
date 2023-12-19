import unittest

from tests.setup import to_dwc

LABEL = "lat_long"


class TestLatLong(unittest.TestCase):
    def test_lat_long_dwc_01(self):
        verb = "40.104905N, 79.324561W NAD83"
        self.assertEqual(
            to_dwc(LABEL, "floodplain wetland. " + verb),
            {"dwc:verbatimCoordinates": verb, "dwc:geodeticDatum": "NAD83"},
        )

    def test_lat_long_dwc_02(self):
        verb = "43.963272° N, 113.446226° W Uncertainty: 100 m."
        self.assertEqual(
            to_dwc(LABEL, verb),
            {
                "dwc:verbatimCoordinates": verb,
                "dwc:coordinateUncertaintyInMeters": 100.0,
            },
        )
