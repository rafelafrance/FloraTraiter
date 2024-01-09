import unittest

from tests.setup import to_dwc

LABEL = "elevation"


class TestElevation(unittest.TestCase):
    def test_elevation_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Elev: 782m. (2566 ft)"),
            {
                "dwc:verbatimElevation": "Elev: 782m. (2566 ft)",
                "dwc:minimumElevationInMeters": 782.0,
            },
        )

    def test_elevation_dwc_02(self):
        self.assertEqual(
            to_dwc(LABEL, "Elev. ca. 460 - 470 m"),
            {
                "dwc:verbatimElevation": "Elev. ca. 460 - 470 m",
                "dwc:minimumElevationInMeters": 460.0,
                "dwc:maximumElevationInMeters": 470.0,
                "dwc:dynamicProperties": {"elevationUncertain": "uncertain"},
            },
        )
