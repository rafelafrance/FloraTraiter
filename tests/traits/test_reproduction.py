import unittest

from tests.setup import test


class TestReproduction(unittest.TestCase):
    def test_reproduction_01(self):
        self.assertEqual(
            test(
                """
                bisexual (unisexual and plants sometimes gynodioecious,
                or plants dioecious"""
            ),
            [
                {"sex": "bisexual", "trait": "sex", "start": 0, "end": 8},
                {"sex": "unisexual", "trait": "sex", "start": 10, "end": 19},
                {
                    "plant_part": "plant",
                    "trait": "plant_part",
                    "start": 24,
                    "end": 30,
                    "sex": "unisexual",
                },
                {
                    "reproduction": "gynodioecious",
                    "trait": "reproduction",
                    "start": 41,
                    "end": 54,
                },
                {
                    "plant_part": "plant",
                    "trait": "plant_part",
                    "start": 59,
                    "end": 65,
                    "sex": "unisexual",
                },
                {
                    "reproduction": "dioecious",
                    "trait": "reproduction",
                    "start": 66,
                    "end": 75,
                },
            ],
        )
