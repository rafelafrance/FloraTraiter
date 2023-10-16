import unittest

from tests.setup import small_test


class TestSurface(unittest.TestCase):
    def test_surface_01(self):
        self.assertEqual(
            small_test("""glabrous flowers"""),
            [
                {
                    "surface": "glabrous",
                    "trait": "surface",
                    "start": 0,
                    "end": 8,
                    "flower_part": "flower",
                },
                {
                    "flower_part": "flower",
                    "trait": "flower_part",
                    "start": 9,
                    "end": 16,
                },
            ],
        )
