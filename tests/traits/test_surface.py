import unittest

from flora.pylib.traits.part import Part
from flora.pylib.traits.surface import Surface
from tests.setup import test


class TestSurface(unittest.TestCase):
    def test_surface_01(self):
        self.assertEqual(
            test("""glabrous flowers"""),
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
