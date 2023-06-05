import unittest

from tests.setup import test


class TestPart(unittest.TestCase):
    def test_part_01(self):
        self.assertEqual(
            test("with thick, woody rootstock."),
            [
                {
                    "woodiness": "woody",
                    "trait": "woodiness",
                    "plant_part": "rootstock",
                    "start": 12,
                    "end": 17,
                },
                {
                    "plant_part": "rootstock",
                    "trait": "plant_part",
                    "start": 18,
                    "end": 27,
                },
            ],
        )

    def test_part_02(self):
        self.assertEqual(
            test("leaflets mostly 1 or 3"),
            [
                {"leaf_part": "leaflet", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "low": 1,
                    "high": 3,
                    "trait": "count",
                    "leaf_part": "leaflet",
                    "start": 16,
                    "end": 22,
                },
            ],
        )

    def test_part_03(self):
        self.assertEqual(
            test("Receptacle discoid."),
            [
                {
                    "flower_part": "receptacle",
                    "trait": "flower_part",
                    "start": 0,
                    "end": 10,
                },
                {
                    "shape": "disk",
                    "trait": "shape",
                    "start": 11,
                    "end": 18,
                    "flower_part": "receptacle",
                },
            ],
        )

    def test_part_04(self):
        self.assertEqual(
            test("Flowers: sepals (pistillate)"),
            [
                {"flower_part": "flower", "trait": "flower_part", "start": 0, "end": 7},
                {
                    "flower_part": "sepal",
                    "trait": "flower_part",
                    "start": 9,
                    "end": 15,
                    "sex": "pistillate",
                },
                {"sex": "pistillate", "trait": "sex", "start": 16, "end": 28},
            ],
        )

    def test_part_05(self):
        self.assertEqual(
            test("Flowers: staminate:"),
            [
                {
                    "flower_part": "flower",
                    "trait": "flower_part",
                    "start": 0,
                    "end": 7,
                },
                {
                    "sex": "staminate",
                    "trait": "sex",
                    "start": 9,
                    "end": 18,
                },
            ],
        )

    def test_part_06(self):
        self.assertEqual(
            test("Heads more than 2-flowered"),
            [
                {
                    "inflorescence": "head",
                    "trait": "inflorescence",
                    "start": 0,
                    "end": 5,
                },
                {
                    "low": 2,
                    "subpart": "flower",
                    "inflorescence": "head",
                    "trait": "count",
                    "start": 16,
                    "end": 26,
                },
            ],
        )

    def test_part_07(self):
        self.assertEqual(
            test("Phyllodes glaucous"),
            [
                {"leaf_part": "phyllode", "trait": "leaf_part", "start": 0, "end": 9},
            ],
        )

    def test_part_08(self):
        self.assertEqual(
            test("""stems and lf-axes hispid"""),
            [
                {
                    "trait": "multiple_parts",
                    "start": 0,
                    "end": 17,
                    "multiple_parts": ["stem", "leaf-axis"],
                },
                {
                    "surface": "hispid",
                    "trait": "surface",
                    "start": 18,
                    "end": 24,
                    "multiple_parts": ["stem", "leaf-axis"],
                },
            ],
        )

    def test_part_09(self):
        self.assertEqual(
            test("""no paraphyllidia"""),
            [
                {
                    "end": 16,
                    "missing_part": "no paraphyllidia",
                    "start": 0,
                    "trait": "missing_part",
                },
            ],
        )
