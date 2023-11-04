import unittest

from tests.setup import to_dwc

LABEL = "count"


class TestColor(unittest.TestCase):
    def test_count_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Seeds [1–]3–12[–30]."),
            {
                "dwc:dynamicProperties": {
                    "seedCount": "minimum: 1 ~ low: 3 ~ high: 12 ~ maximum: 30"
                }
            },
        )

    def test_count_dwc_02(self):
        self.assertEqual(
            to_dwc(LABEL, "Staminate flowers 5–10"),
            {"dwc:dynamicProperties": {"staminateFlowerCount": "low: 5 ~ high: 10"}},
        )

    def test_count_dwc_03(self):
        self.assertEqual(
            to_dwc(LABEL, "leaflets in 3 or 4 pairs"),
            {
                "dwc:dynamicProperties": {
                    "leafletCount": "low: 3 ~ high: 4 ~ group: pairs"
                }
            },
        )

    def test_count_dwc_04(self):
        self.assertEqual(
            to_dwc(LABEL, "Seeds (1 or)2 or 3 per legume,"),
            {
                "dwc:dynamicProperties": {
                    "seedCount": "minimum: 1 ~ low: 2 ~ high: 3 ~ perPart: legume"
                }
            },
        )
