import unittest

from tests.setup import to_dwc

LABEL = "count"


class TestColor(unittest.TestCase):
    def test_count_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Seeds [1–]3–12[–30]."),
            {
                "dwc:dynamicProperties": {
                    "seedCountMinimum": 1,
                    "seedCountLow": 3,
                    "seedCountHigh": 12,
                    "seedCountMaximum": 30,
                },
            },
        )

    def test_count_dwc_02(self):
        self.assertEqual(
            to_dwc(LABEL, "Staminate flowers 5–10"),
            {
                "dwc:dynamicProperties": {
                    "staminateFlowerCountLow": 5,
                    "staminateFlowerCountHigh": 10,
                }
            },
        )

    def test_count_dwc_03(self):
        self.assertEqual(
            to_dwc(LABEL, "leaflets in 3 or 4 pairs"),
            {
                "dwc:dynamicProperties": {
                    "leafletCountGroup": "pairs",
                    "leafletCountLow": 3,
                    "leafletCountHigh": 4,
                }
            },
        )

    def test_count_dwc_04(self):
        self.assertEqual(
            to_dwc(LABEL, "Seeds (1 or)2 or 3 per legume,"),
            {
                "dwc:dynamicProperties": {
                    "seedCountPerPart": "legume",
                    "seedCountMinimum": 1,
                    "seedCountLow": 2,
                    "seedCountHigh": 3,
                }
            },
        )
