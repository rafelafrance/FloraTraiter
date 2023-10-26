import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "count"


class TestColor(unittest.TestCase):
    def test_count_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Seeds [1–]3–12[–30].")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {
                    "seedCountMinimum": 1,
                    "seedCountLow": 3,
                    "seedCountHigh": 12,
                    "seedCountMaximum": 30,
                },
            },
        )

    def test_count_dwc_02(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Staminate flowers 5–10")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {
                    "staminateFlowerCountLow": 5,
                    "staminateFlowerCountHigh": 10,
                }
            },
        )

    def test_count_dwc_03(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "leaflets in 3 or 4 pairs")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {
                    "leafletCountGroup": "pairs",
                    "leafletCountLow": 3,
                    "leafletCountHigh": 4,
                }
            },
        )

    def test_count_dwc_04(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Seeds (1 or)2 or 3 per legume,")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {
                    "seedCountPerPart": "legume",
                    "seedCountMinimum": 1,
                    "seedCountLow": 2,
                    "seedCountHigh": 3,
                }
            },
        )
