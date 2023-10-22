import unittest

from flora.pylib.traits.location import Location
from flora.pylib.traits.part import Part
from flora.pylib.traits.surface import Surface
from tests.setup import test


class TestLocation(unittest.TestCase):
    def test_location_01(self):
        self.maxDiff = None
        self.assertEqual(
            test("""setose their whole length dorsally and the flowers are smaller"""),
            [
                Surface(
                    surface="setose",
                    trait="surface",
                    start=0,
                    end=6,
                    part="flower",
                    location="dorsal",
                ),
                Location(
                    trait="location",
                    type="part_location",
                    location="dorsal",
                    start=26,
                    end=34,
                ),
                Part(
                    part="flower",
                    trait="part",
                    start=43,
                    end=50,
                    location="dorsal",
                    type="flower_part",
                ),
            ],
        )
