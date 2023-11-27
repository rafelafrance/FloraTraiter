import unittest

from flora.pylib.rules.part_location import PartLocation
from flora.pylib.rules.shape import Shape
from flora.pylib.rules.subpart import Subpart
from tests.setup import parse


class TestSubpart(unittest.TestCase):
    def test_subpart_01(self):
        self.assertEqual(
            parse("terminal lobe ovate-trullate,"),
            [
                PartLocation(
                    trait="part_location",
                    start=0,
                    end=8,
                    part_location="terminal",
                    type="part_location",
                ),
                Subpart(
                    trait="subpart",
                    subpart="lobe",
                    start=9,
                    end=13,
                    part_location="terminal",
                ),
                Shape(
                    shape="ovate-trullate",
                    trait="shape",
                    start=14,
                    end=28,
                    subpart="lobe",
                    part_location="terminal",
                ),
            ],
        )
