import unittest

from tests.setup import test


class TestPartLinker(unittest.TestCase):
    def test_part_linker_01(self):
        self.assertEqual(
            test("""pinnules up to 31 pairs,"""),
            [
                {"leaf_part": "pinnule", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "low": 31,
                    "trait": "count",
                    "start": 15,
                    "end": 23,
                    "count_group": "pairs",
                    "leaf_part": "pinnule",
                },
            ],
        )

    def test_part_linker_02(self):
        self.assertEqual(
            test(
                """trees closely resembling another thing in habit,
                attaining 2-4 m in height with trunk"""
            ),
            [
                {"plant_part": "tree", "trait": "plant_part", "start": 0, "end": 5},
                {
                    "dimensions": "height",
                    "height_low": 200.0,
                    "height_high": 400.0,
                    "trait": "size",
                    "start": 59,
                    "end": 74,
                    "units": "cm",
                    "plant_part": "trunk",
                },
                {"plant_part": "trunk", "trait": "plant_part", "start": 80, "end": 85},
            ],
        )

    def test_part_linker_03(self):
        self.assertEqual(
            test(
                """Pods here are some words, and more words, we keep writing things
                 until the desired part is far away from its size 25-35 X 12-18 mm,
                 the replum 1.5-2 mm wide,"""
            ),
            [
                {"fruit_part": "pod", "trait": "fruit_part", "start": 0, "end": 4},
                {
                    "dimensions": ["length", "width"],
                    "length_low": 2.5,
                    "length_high": 3.5,
                    "width_low": 1.2,
                    "width_high": 1.8,
                    "trait": "size",
                    "start": 114,
                    "end": 130,
                    "units": "cm",
                    "fruit_part": "pod",
                },
                {
                    "fruit_part": "replum",
                    "trait": "fruit_part",
                    "start": 136,
                    "end": 142,
                },
                {
                    "dimensions": "width",
                    "width_low": 0.15,
                    "width_high": 0.2,
                    "trait": "size",
                    "start": 143,
                    "end": 156,
                    "units": "cm",
                    "fruit_part": "replum",
                },
            ],
        )

    def test_part_linker_04(self):
        self.maxDiff = None
        self.assertEqual(
            test(
                """Lvs (except of A. pachyphloia) bipinnate, the primary and secondary
                axes normally pulvinate (the primary pulvinus rarely suppressed)"""
            ),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 3},
                {
                    "rank": "species",
                    "taxon": "Acacia pachyphloia",
                    "trait": "taxon",
                    "start": 15,
                    "end": 29,
                },
                {
                    "shape": "bipinnate",
                    "trait": "shape",
                    "start": 31,
                    "end": 40,
                    "leaf_part": "leaf",
                },
                {
                    "subpart": "axis",
                    "trait": "subpart",
                    "start": 58,
                    "end": 72,
                    "leaf_part": "pulvinus",
                },
                {
                    "shape": "pulvinate",
                    "trait": "shape",
                    "start": 82,
                    "end": 91,
                    "leaf_part": "pulvinus",
                    "subpart": "axis",
                },
                {
                    "trait": "leaf_part",
                    "start": 97,
                    "end": 113,
                    "leaf_part": "pulvinus",
                },
            ],
        )

    def test_part_linker_05(self):
        self.assertEqual(
            test("""juvenile leaves persistent for a long period."""),
            [
                {"end": 15, "leaf_part": "leaf", "start": 9, "trait": "leaf_part"},
                {
                    "duration": "persistent",
                    "end": 26,
                    "start": 16,
                    "trait": "duration",
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_part_linker_06(self):
        self.assertEqual(
            test("""Most species have stipular spines, bipinnately compound leaves."""),
            [
                {
                    "leaf_part": "stipular spine",
                    "trait": "leaf_part",
                    "start": 18,
                    "end": 33,
                },
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 56, "end": 62},
            ],
        )
