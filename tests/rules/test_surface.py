import unittest

from flora.pylib.rules.part import Part
from flora.pylib.rules.surface import Surface
from tests.setup import parse


class TestSurface(unittest.TestCase):
    def test_surface_01(self):
        self.assertEqual(
            parse("""glabrous flowers"""),
            [
                Surface(
                    surface="glabrous",
                    trait="surface",
                    start=0,
                    end=8,
                    part="flower",
                ),
                Part(
                    part="flower",
                    type="flower_part",
                    trait="part",
                    start=9,
                    end=16,
                ),
            ],
        )
