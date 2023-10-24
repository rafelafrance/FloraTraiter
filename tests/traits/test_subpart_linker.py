import unittest

from flora.pylib.traits.count import Count
from flora.pylib.traits.part import Part
from flora.pylib.traits.shape import Shape
from flora.pylib.traits.subpart import Subpart
from flora.pylib.traits.surface import Surface
from tests.setup import test


class TestSubpartLinker(unittest.TestCase):
    def test_subpart_linker_01(self):
        self.assertEqual(
            test("""limbs (1-) 2-4 (-5) pairs;"""),
            [
                Subpart(subpart="limb", trait="subpart", start=0, end=5),
                Count(
                    min=1,
                    low=2,
                    high=4,
                    max=5,
                    trait="count",
                    start=6,
                    end=25,
                    count_group="pairs",
                    subpart="limb",
                ),
            ],
        )

    def test_subpart_linker_02(self):
        self.assertEqual(
            test("""blades oblong setose-ciliolate"""),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Shape(
                    shape="oblong",
                    trait="shape",
                    subpart="ciliolate",
                    start=7,
                    end=13,
                    part="leaf",
                ),
                Surface(
                    surface="setose",
                    subpart="ciliolate",
                    trait="surface",
                    start=14,
                    end=20,
                    part="leaf",
                ),
                Subpart(
                    subpart="ciliolate",
                    part="leaf",
                    trait="subpart",
                    start=20,
                    end=30,
                ),
            ],
        )
