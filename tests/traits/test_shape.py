import unittest

from tests.setup import test


class TestShape(unittest.TestCase):
    def test_shape_01(self):
        self.assertEqual(
            test("leaf suborbiculate"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "shape": "orbicular",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 5,
                    "end": 18,
                },
            ],
        )

    def test_shape_02(self):
        self.assertEqual(
            test("leaf ovate-suborbicular"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "shape": "ovate-orbicular",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 5,
                    "end": 23,
                },
            ],
        )

    def test_shape_03(self):
        self.assertEqual(
            test("petiolule narrowly oblanceolate,"),
            [
                {"leaf_part": "petiolule", "trait": "leaf_part", "start": 0, "end": 9},
                {
                    "shape": "oblanceolate",
                    "trait": "shape",
                    "leaf_part": "petiolule",
                    "start": 10,
                    "end": 31,
                },
            ],
        )

    def test_shape_04(self):
        self.assertEqual(
            test("Leaves ; blade ovate or orbiculate to suborbiculate or reniform,"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 9, "end": 14},
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 15,
                    "end": 20,
                },
                {
                    "shape": "orbicular",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 24,
                    "end": 34,
                },
                {
                    "shape": "orbicular",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 38,
                    "end": 51,
                },
                {
                    "shape": "reniform",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 55,
                    "end": 63,
                },
            ],
        )

    def test_shape_05(self):
        self.assertEqual(
            test(
                """
                Leaves: blade ovate or elongate-ovate to
                lanceolate-ovate or ovate-triangular,"""
            ),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 8, "end": 13},
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 14,
                    "end": 19,
                },
                {
                    "shape": "elongate-ovate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 23,
                    "end": 37,
                },
                {
                    "shape": "lanceolate-ovate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 41,
                    "end": 57,
                },
                {
                    "shape": "ovate-triangular",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 61,
                    "end": 77,
                },
            ],
        )

    def test_shape_06(self):
        self.assertEqual(
            test("Leaves: blade broadly to shallowly triangular"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 8, "end": 13},
                {
                    "shape": "triangular",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 14,
                    "end": 45,
                },
            ],
        )

    def test_shape_07(self):
        self.assertEqual(
            test(
                """
                ; blade abaxially, suborbiculate to
                broadly ovate, depressed-ovate, or reniform,"""
            ),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 2, "end": 7},
                {
                    "shape": "orbicular",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 19,
                    "end": 32,
                },
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 36,
                    "end": 49,
                },
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 51,
                    "end": 66,
                },
                {
                    "shape": "reniform",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 71,
                    "end": 79,
                },
            ],
        )

    def test_shape_08(self):
        self.assertEqual(
            test(
                """
                blade broadly ovate-cordate to triangular-cordate or
                reniform, shallowly to deeply palmately"""
            ),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 5},
                {
                    "shape": "ovate-cordate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 6,
                    "end": 27,
                },
                {
                    "shape": "triangular-cordate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 31,
                    "end": 49,
                },
                {
                    "shape": "reniform",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 53,
                    "end": 61,
                },
            ],
        )

    def test_shape_09(self):
        self.assertEqual(
            test("Leaf blades lobe apex rounded"),
            [
                {
                    "trait": "subpart",
                    "subpart": "leaf lobe apex",
                    "start": 0,
                    "end": 21,
                },
                {
                    "shape": "orbicular",
                    "trait": "shape",
                    "start": 22,
                    "end": 29,
                    "subpart": "leaf lobe apex",
                },
            ],
        )

    def test_shape_10(self):
        self.assertEqual(
            test("Leaf blades mostly orbiculate, deeply to shallowly lobed,"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 11},
                {
                    "shape": "orbicular",
                    "trait": "shape",
                    "start": 12,
                    "end": 29,
                    "leaf_part": "leaf",
                },
                {
                    "subpart": "lobe",
                    "trait": "subpart",
                    "start": 51,
                    "end": 56,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_shape_11(self):
        self.assertEqual(
            test(
                """
                Leaves: petiole blade pentagonal-angulate to
                reniform-angulate or shallowly 5-angulate."""
            ),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "leaf_part": "petiole leaf",
                    "trait": "leaf_part",
                    "start": 8,
                    "end": 21,
                },
                {
                    "shape": "polygonal",
                    "trait": "shape",
                    "start": 22,
                    "end": 41,
                    "leaf_part": "petiole leaf",
                },
                {
                    "shape": "reniform-polygonal",
                    "trait": "shape",
                    "start": 45,
                    "end": 62,
                    "leaf_part": "petiole leaf",
                },
                {
                    "shape": "polygonal",
                    "trait": "shape",
                    "start": 66,
                    "end": 86,
                    "leaf_part": "petiole leaf",
                },
            ],
        )

    def test_shape_12(self):
        self.assertEqual(
            test(
                """
                blade lanceolate to narrowly or broadly lanceolate
                or elliptic-lanceolate,"""
            ),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 5},
                {
                    "shape": "lanceolate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 6,
                    "end": 16,
                },
                {
                    "shape": "lanceolate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 32,
                    "end": 50,
                },
                {
                    "shape": "elliptic-lanceolate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 54,
                    "end": 73,
                },
            ],
        )

    def test_shape_13(self):
        self.assertEqual(
            test("blade broadly ovate to rounded-cordate, subreniform, or deltate"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 5},
                {
                    "shape": "ovate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 6,
                    "end": 19,
                },
                {
                    "shape": "orbicular-cordate",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 23,
                    "end": 38,
                },
                {
                    "shape": "reniform",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 40,
                    "end": 51,
                },
                {
                    "shape": "deltoid",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 56,
                    "end": 63,
                },
            ],
        )

    def test_shape_14(self):
        self.assertEqual(
            test("blade orbiculate to pentagonal,"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 5},
                {
                    "shape": "orbicular",
                    "trait": "shape",
                    "start": 6,
                    "end": 16,
                    "leaf_part": "leaf",
                },
                {
                    "shape": "polygonal",
                    "trait": "shape",
                    "start": 20,
                    "end": 30,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_shape_15(self):
        self.assertEqual(
            test("Petals standard rhombic-elliptic to obovate,"),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "shape": "rhomboic-elliptic",
                    "trait": "shape",
                    "flower_part": "petal",
                    "start": 16,
                    "end": 32,
                },
                {
                    "shape": "obovate",
                    "trait": "shape",
                    "flower_part": "petal",
                    "start": 36,
                    "end": 43,
                },
            ],
        )

    def test_shape_16(self):
        self.assertEqual(
            test("<base truncate to cordate>"),
            [
                {"subpart": "base", "trait": "subpart", "start": 1, "end": 5},
                {
                    "shape": "truncate",
                    "trait": "shape",
                    "subpart": "base",
                    "start": 6,
                    "end": 14,
                },
                {
                    "shape": "cordate",
                    "trait": "shape",
                    "subpart": "base",
                    "start": 18,
                    "end": 25,
                },
            ],
        )

    def test_shape_17(self):
        self.assertEqual(
            test("Seeds globose-angular"),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "shape": "spheric-angular",
                    "trait": "shape",
                    "fruit_part": "seed",
                    "start": 6,
                    "end": 21,
                },
            ],
        )

    def test_shape_18(self):
        self.assertEqual(
            test("bractlets narrowly to broadly ovate-triangular"),
            [
                {"leaf_part": "bract", "trait": "leaf_part", "start": 0, "end": 9},
                {
                    "shape": "ovate-triangular",
                    "trait": "shape",
                    "leaf_part": "bract",
                    "start": 10,
                    "end": 46,
                },
            ],
        )

    def test_shape_19(self):
        self.assertEqual(
            test("Petals purple; bilobate;"),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "start": 15,
                    "end": 23,
                    "trait": "shape",
                    "shape": "bilobate",
                    "flower_part": "petal",
                },
            ],
        )

    def test_shape_20(self):
        self.assertEqual(
            test("blade broadly ovate-angulate to reniform-angulate"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 5},
                {
                    "shape": "ovate-polygonal",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 6,
                    "end": 28,
                },
                {
                    "shape": "reniform-polygonal",
                    "trait": "shape",
                    "leaf_part": "leaf",
                    "start": 32,
                    "end": 49,
                },
            ],
        )

    def test_shape_21(self):
        self.assertEqual(
            test("leaf subflabellate"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "venation": "subflabellate",
                    "trait": "venation",
                    "leaf_part": "leaf",
                    "start": 5,
                    "end": 18,
                },
            ],
        )

    def test_shape_22(self):
        self.assertEqual(
            test("partly confluent or branched blade"),
            [
                {
                    "shape": "confluent",
                    "trait": "shape",
                    "start": 0,
                    "end": 16,
                    "leaf_part": "leaf",
                },
                {
                    "shape": "branched",
                    "trait": "shape",
                    "start": 20,
                    "end": 28,
                    "leaf_part": "leaf",
                },
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 29, "end": 34},
            ],
        )
