import unittest

from flora.pylib.rules.count import Count
from flora.pylib.rules.duration import Duration
from flora.pylib.rules.part import Part
from flora.pylib.rules.shape import Shape
from flora.pylib.rules.size import Dimension
from flora.pylib.rules.size import Size
from flora.pylib.rules.subpart import Subpart
from flora.pylib.rules.taxon import Taxon
from tests.setup import parse


class TestPartLinker(unittest.TestCase):
    def test_part_linker_01(self):
        self.assertEqual(
            parse("""pinnules up to 31 pairs,"""),
            [
                Part(part="pinnule", trait="part", type="leaf_part", start=0, end=8),
                Count(
                    low=31,
                    trait="count",
                    start=15,
                    end=23,
                    count_group="pairs",
                    part="pinnule",
                ),
            ],
        )

    def test_part_linker_02(self):
        self.assertEqual(
            parse(
                """trees closely resembling another thing in habit,
                attaining 2-4 m in height with trunk"""
            ),
            [
                Part(part="tree", trait="part", type="plant_part", start=0, end=5),
                Size(
                    dims=[Dimension(dim="height", low=200.0, high=400.0)],
                    trait="size",
                    start=59,
                    end=74,
                    units="cm",
                    part="tree",
                ),
                Part(part="trunk", trait="part", type="plant_part", start=80, end=85),
            ],
        )

    def test_part_linker_03(self):
        # self.maxDiff = None
        self.assertEqual(
            parse(
                """Pods here are some words, and more words, we keep writing things
                 until the desired part is far away from its size 25-35 X 12-18 mm,
                 the replum 1.5-2 mm wide,"""
            ),
            [
                Part(part="pod", trait="part", type="fruit_part", start=0, end=4),
                Size(
                    dims=[
                        Dimension("length", low=2.5, high=3.5),
                        Dimension("width", low=1.2, high=1.8),
                    ],
                    trait="size",
                    start=114,
                    end=130,
                    units="cm",
                    part="pod",
                ),
                Part(
                    part="replum",
                    trait="part",
                    type="fruit_part",
                    start=136,
                    end=142,
                ),
                Size(
                    dims=[Dimension("width", low=0.15, high=0.2)],
                    trait="size",
                    start=143,
                    end=156,
                    units="cm",
                    part="replum",
                ),
            ],
        )

    def test_part_linker_04(self):
        self.assertEqual(
            parse(
                """Lvs (except of A. pachyphloia) bipinnate, the primary and secondary
                axes normally pulvinate (the primary pulvinus rarely suppressed)"""
            ),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=3),
                Taxon(
                    rank="species",
                    taxon="Acacia pachyphloia",
                    trait="taxon",
                    start=15,
                    end=29,
                ),
                Shape(
                    shape="bipinnate",
                    trait="shape",
                    start=31,
                    end=40,
                    part="leaf",
                ),
                Subpart(
                    subpart="axis",
                    trait="subpart",
                    start=68,
                    end=72,
                    part="pulvinus",
                ),
                Shape(
                    shape="pulvinate",
                    trait="shape",
                    start=82,
                    end=91,
                    part="pulvinus",
                    subpart="axis",
                ),
                Part(
                    trait="part",
                    type="leaf_part",
                    start=97,
                    end=113,
                    part="pulvinus",
                ),
            ],
        )

    def test_part_linker_05(self):
        self.assertEqual(
            parse("""juvenile leaves persistent for a long period."""),
            [
                Part(end=15, part="leaf", start=9, trait="part", type="leaf_part"),
                Duration(
                    duration="persistent",
                    part="leaf",
                    end=26,
                    start=16,
                    trait="duration",
                ),
            ],
        )

    def test_part_linker_06(self):
        self.assertEqual(
            parse(
                """Most species have stipular spines, bipinnately compound leaves."""
            ),
            [
                Part(
                    part="stipular spines",
                    trait="part",
                    type="leaf_part",
                    start=18,
                    end=33,
                ),
                Part(part="leaf", trait="part", type="leaf_part", start=56, end=62),
            ],
        )
