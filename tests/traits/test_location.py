import unittest

from tests.setup import test


class TestLocation(unittest.TestCase):
    def test_location_01(self):
        self.assertEqual(
            test("""setose their whole length dorsally and the flowers are smaller"""),
            [
                {
                    "surface": "setose",
                    "trait": "surface",
                    "start": 0,
                    "end": 6,
                    "flower_part": "flower",
                    "location": "dorsal",
                },
                {
                    "flower_part": "flower",
                    "trait": "flower_part",
                    "start": 43,
                    "end": 50,
                    "location": "dorsal",
                },
            ],
        )
