import unittest

from flora.pylib.traits.part_location import PartLocation
from flora.pylib.traits.shape import Shape
from flora.pylib.traits.subpart import Subpart
from tests.setup import test


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self):
        self.assertEqual(
            test("terminal lobe ovate-trullate,"),
            [
                PartLocation(
                    trait="location",
                    start=0,
                    end=8,
                    location="terminal",
                    type="part_location",
                ),
                Subpart(
                    trait="subpart",
                    subpart="lobe",
                    start=9,
                    end=13,
                    location="terminal",
                ),
                Shape(
                    shape="ovate-trullate",
                    trait="shape",
                    start=14,
                    end=28,
                    subpart="lobe",
                    location="terminal",
                ),
            ],
        )
