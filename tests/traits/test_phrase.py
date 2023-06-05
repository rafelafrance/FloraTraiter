import unittest

from tests.setup import test


class TestPhrase(unittest.TestCase):
    def test_phrase_01(self):
        self.assertEqual(
            test("Pistillate flowers usually sessile; hypogynous"),
            [
                {
                    "sex": "pistillate",
                    "trait": "sex",
                    "start": 0,
                    "end": 10,
                },
                {
                    "flower_part": "flower",
                    "trait": "flower_part",
                    "start": 11,
                    "end": 18,
                    "sex": "pistillate",
                },
                {
                    "flower_location": "superior",
                    "trait": "flower_location",
                    "start": 36,
                    "end": 46,
                },
            ],
        )

    def test_phrase_02(self):
        self.assertEqual(
            test("Petals glabrous, deciduous;"),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "surface": "glabrous",
                    "trait": "surface",
                    "start": 7,
                    "end": 15,
                    "flower_part": "petal",
                },
                {
                    "leaf_duration": "deciduous",
                    "trait": "leaf_duration",
                    "start": 17,
                    "end": 26,
                },
            ],
        )

    def test_phrase_03(self):
        self.assertEqual(
            test("leaf blade herbaceous."),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 10},
                {
                    "woodiness": "herbaceous",
                    "trait": "woodiness",
                    "start": 11,
                    "end": 21,
                    "leaf_part": "leaf",
                },
            ],
        )
