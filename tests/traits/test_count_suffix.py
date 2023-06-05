import unittest

from tests.setup import test


class TestCountSuffix(unittest.TestCase):
    def test_count_suffix_01(self):
        self.assertEqual(
            test("leaf rarely 1- or 5-7-foliolate;"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "min": 1,
                    "low": 5,
                    "max": 7,
                    "trait": "count",
                    "start": 5,
                    "end": 31,
                    "subpart": "lobe",
                    "missing": True,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_count_suffix_02(self):
        self.assertEqual(
            test("Leaves imparipinnate, 5- or 7(or 9)-foliolate;"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "shape": "imparipinnate",
                    "trait": "shape",
                    "start": 7,
                    "end": 20,
                    "leaf_part": "leaf",
                },
                {
                    "low": 5,
                    "high": 7,
                    "max": 9,
                    "trait": "count",
                    "start": 22,
                    "end": 45,
                    "subpart": "lobe",
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_count_suffix_03(self):
        self.assertEqual(
            test("Racemes compact, 1- or 2- or 5-7-flowered"),
            [
                {
                    "inflorescence": "raceme",
                    "trait": "inflorescence",
                    "start": 0,
                    "end": 7,
                },
                {
                    "min": 1,
                    "low": 2,
                    "high": 5,
                    "max": 7,
                    "trait": "count",
                    "start": 17,
                    "end": 41,
                    "inflorescence": "raceme",
                    "subpart": "flower",
                },
            ],
        )

    def test_count_suffix_04(self):
        self.assertEqual(
            test("leaf 3(or 5-9)-foliolate;"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "min": 3,
                    "low": 5,
                    "high": 9,
                    "trait": "count",
                    "start": 5,
                    "end": 24,
                    "subpart": "lobe",
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_count_suffix_05(self):
        self.assertEqual(
            test("leaflets (2or)3- or 4(or 5)-paired"),
            [
                {"leaf_part": "leaflet", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "min": 2,
                    "low": 3,
                    "high": 4,
                    "max": 5,
                    "trait": "count",
                    "start": 9,
                    "end": 34,
                    "count_group": "pairs",
                    "leaf_part": "leaflet",
                },
            ],
        )

    def test_count_suffix_06(self):
        self.assertEqual(
            test("Leaves (19-)23- or 25-foliolate;"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "min": 19,
                    "low": 23,
                    "high": 25,
                    "trait": "count",
                    "start": 7,
                    "end": 31,
                    "subpart": "lobe",
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_count_suffix_07(self):
        self.assertEqual(
            test("Calyx (5-lobed)"),
            [
                {"flower_part": "calyx", "trait": "flower_part", "start": 0, "end": 5},
                {
                    "low": 5,
                    "trait": "count",
                    "start": 7,
                    "end": 14,
                    "subpart": "lobe",
                    "flower_part": "calyx",
                },
            ],
        )

    def test_count_suffix_08(self):
        self.assertEqual(
            test("Inflorescences 1–64(–90)[–100]-flowered"),
            [
                {
                    "inflorescence": "inflorescence",
                    "trait": "inflorescence",
                    "start": 0,
                    "end": 14,
                },
                {
                    "min": 1,
                    "low": 64,
                    "high": 90,
                    "max": 100,
                    "trait": "count",
                    "start": 15,
                    "end": 39,
                    "inflorescence": "inflorescence",
                    "subpart": "flower",
                },
            ],
        )

    def test_count_suffix_09(self):
        self.assertEqual(
            test("""Cymes [1–]few[–many]-flowered."""),
            [
                {
                    "inflorescence": "cyme",
                    "trait": "inflorescence",
                    "start": 0,
                    "end": 5,
                },
                {
                    "low": 1,
                    "trait": "count",
                    "start": 6,
                    "end": 29,
                    "inflorescence": "cyme",
                    "subpart": "flower",
                },
            ],
        )

    def test_count_suffix_10(self):
        self.assertEqual(
            test("""Capsules [2–]3[–5+]-locular."""),
            [
                {"fruit_part": "capsule", "trait": "fruit_part", "start": 0, "end": 8},
                {
                    "min": 2,
                    "low": 3,
                    "max": 5,
                    "trait": "count",
                    "start": 9,
                    "end": 27,
                    "subpart": "locular",
                    "fruit_part": "capsule",
                },
            ],
        )

    def test_count_suffix_11(self):
        self.assertEqual(
            test("""Flowers mostly 4- or 5-merous"""),
            [
                {"flower_part": "flower", "trait": "flower_part", "start": 0, "end": 7},
                {
                    "low": 4,
                    "high": 5,
                    "trait": "count",
                    "start": 15,
                    "end": 29,
                    "count": "merous",
                    "flower_part": "flower",
                },
            ],
        )

    def test_count_suffix_12(self):
        self.assertEqual(
            test("""Capsule 2-locular. x = 9."""),
            [
                {"fruit_part": "capsule", "trait": "fruit_part", "start": 0, "end": 7},
                {
                    "low": 2,
                    "trait": "count",
                    "start": 8,
                    "end": 17,
                    "subpart": "locular",
                    "fruit_part": "capsule",
                },
            ],
        )

    def test_count_suffix_13(self):
        self.assertEqual(
            test("""pinnae 16-29-jug."""),
            [
                {"leaf_part": "pinnae", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "low": 16,
                    "high": 29,
                    "trait": "count",
                    "start": 7,
                    "end": 17,
                    "count_group": "pairs",
                    "leaf_part": "pinnae",
                },
            ],
        )

    def test_count_suffix_14(self):
        self.assertEqual(
            test("""4-6-seeded, the replum"""),
            [
                {
                    "low": 4,
                    "high": 6,
                    "trait": "count",
                    "start": 0,
                    "end": 10,
                    "subpart": "seed",
                    "fruit_part": "replum",
                },
                {"fruit_part": "replum", "trait": "fruit_part", "start": 16, "end": 22},
            ],
        )

    def test_count_suffix_15(self):
        self.assertEqual(
            test("""one-seeded replum"""),
            [
                {
                    "low": 1,
                    "trait": "count",
                    "start": 0,
                    "end": 10,
                    "subpart": "seed",
                    "fruit_part": "replum",
                },
                {"fruit_part": "replum", "trait": "fruit_part", "start": 11, "end": 17},
            ],
        )

    def test_count_suffix_16(self):
        self.assertEqual(
            test("""lvs, 1 -nerved"""),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 3},
                {
                    "start": 5,
                    "end": 14,
                    "leaf_part": "leaf",
                    "low": 1,
                    "venation": "vein",
                    "trait": "count",
                },
            ],
        )

    def test_count_suffix_17(self):
        self.assertEqual(
            test("""lvs few-nerved"""),
            [{"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 3}],
        )
