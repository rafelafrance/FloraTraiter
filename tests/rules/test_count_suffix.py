import unittest

from flora.pylib.rules.count import Count
from flora.pylib.rules.part import Part
from flora.pylib.rules.shape import Shape
from tests.setup import parse


class TestCountSuffix(unittest.TestCase):
    def test_count_suffix_01(self):
        self.assertEqual(
            parse("leaf rarely 1- or 5-7-foliolate;"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Count(
                    min=1,
                    low=5,
                    max=7,
                    trait="count",
                    start=5,
                    end=31,
                    subpart="lobe",
                    missing=True,
                    part="leaf",
                ),
            ],
        )

    def test_count_suffix_02(self):
        self.assertEqual(
            parse("Leaves imparipinnate, 5- or 7(or 9)-foliolate;"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Shape(
                    shape="imparipinnate",
                    trait="shape",
                    start=7,
                    end=20,
                    part="leaf",
                ),
                Count(
                    low=5,
                    high=7,
                    max=9,
                    trait="count",
                    start=22,
                    end=45,
                    subpart="lobe",
                    part="leaf",
                ),
            ],
        )

    def test_count_suffix_03(self):
        self.assertEqual(
            parse("Racemes compact, 1- or 2- or 5-7-flowered"),
            [
                Part(
                    part="raceme",
                    trait="part",
                    type="inflorescence",
                    start=0,
                    end=7,
                ),
                Count(
                    min=1,
                    low=2,
                    high=5,
                    max=7,
                    trait="count",
                    start=17,
                    end=41,
                    part="raceme",
                    subpart="flower",
                ),
            ],
        )

    def test_count_suffix_04(self):
        self.assertEqual(
            parse("leaf 3(or 5-9)-foliolate;"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Count(
                    min=3,
                    low=5,
                    high=9,
                    trait="count",
                    start=5,
                    end=24,
                    subpart="lobe",
                    part="leaf",
                ),
            ],
        )

    def test_count_suffix_05(self):
        self.assertEqual(
            parse("leaflets (2or)3- or 4(or 5)-paired"),
            [
                Part(part="leaflet", trait="part", type="leaf_part", start=0, end=8),
                Count(
                    min=2,
                    low=3,
                    high=4,
                    max=5,
                    trait="count",
                    start=9,
                    end=34,
                    count_group="pairs",
                    part="leaflet",
                ),
            ],
        )

    def test_count_suffix_06(self):
        self.assertEqual(
            parse("Leaves (19-)23- or 25-foliolate;"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Count(
                    min=19,
                    low=23,
                    high=25,
                    trait="count",
                    start=7,
                    end=31,
                    subpart="lobe",
                    part="leaf",
                ),
            ],
        )

    def test_count_suffix_07(self):
        self.assertEqual(
            parse("Calyx (5-lobed)"),
            [
                Part(part="calyx", trait="part", type="flower_part", start=0, end=5),
                Count(
                    low=5,
                    trait="count",
                    start=7,
                    end=14,
                    subpart="lobe",
                    part="calyx",
                ),
            ],
        )

    def test_count_suffix_08(self):
        self.assertEqual(
            parse("Inflorescences 1–64(–90)[–100]-flowered"),
            [
                Part(
                    part="inflorescence",
                    trait="part",
                    type="inflorescence",
                    start=0,
                    end=14,
                ),
                Count(
                    min=1,
                    low=64,
                    high=90,
                    max=100,
                    trait="count",
                    start=15,
                    end=39,
                    part="inflorescence",
                    subpart="flower",
                ),
            ],
        )

    def test_count_suffix_09(self):
        self.assertEqual(
            parse("""Cymes [1–]few[–many]-flowered."""),
            [
                Part(
                    part="cyme",
                    trait="part",
                    type="inflorescence",
                    start=0,
                    end=5,
                ),
                Count(
                    low=1,
                    trait="count",
                    start=6,
                    end=29,
                    part="cyme",
                    subpart="flower",
                ),
            ],
        )

    def test_count_suffix_10(self):
        self.assertEqual(
            parse("""Capsules [2–]3[–5+]-locular."""),
            [
                Part(part="capsule", trait="part", type="fruit_part", start=0, end=8),
                Count(
                    min=2,
                    low=3,
                    max=5,
                    trait="count",
                    start=9,
                    end=27,
                    subpart="locular",
                    part="capsule",
                ),
            ],
        )

    def test_count_suffix_11(self):
        self.assertEqual(
            parse("""Flowers mostly 4- or 5-merous"""),
            [
                Part(part="flower", trait="part", type="flower_part", start=0, end=7),
                Count(
                    low=4,
                    high=5,
                    trait="count",
                    start=15,
                    end=29,
                    subpart="merous",
                    part="flower",
                ),
            ],
        )

    def test_count_suffix_12(self):
        self.assertEqual(
            parse("""Capsule 2-locular. x = 9."""),
            [
                Part(part="capsule", trait="part", type="fruit_part", start=0, end=7),
                Count(
                    low=2,
                    trait="count",
                    start=8,
                    end=17,
                    subpart="locular",
                    part="capsule",
                ),
            ],
        )

    def test_count_suffix_13(self):
        self.assertEqual(
            parse("""pinnae 16-29-jug."""),
            [
                Part(part="pinnae", trait="part", type="leaf_part", start=0, end=6),
                Count(
                    low=16,
                    high=29,
                    trait="count",
                    start=7,
                    end=17,
                    count_group="pairs",
                    part="pinnae",
                ),
            ],
        )

    def test_count_suffix_14(self):
        self.assertEqual(
            parse("""4-6-seeded, the replum"""),
            [
                Count(
                    low=4,
                    high=6,
                    trait="count",
                    start=0,
                    end=10,
                    subpart="seed",
                    part="replum",
                ),
                Part(part="replum", trait="part", type="fruit_part", start=16, end=22),
            ],
        )

    def test_count_suffix_15(self):
        self.assertEqual(
            parse("""one-seeded replum"""),
            [
                Count(
                    low=1,
                    trait="count",
                    start=0,
                    end=10,
                    subpart="seed",
                    part="replum",
                ),
                Part(part="replum", trait="part", type="fruit_part", start=11, end=17),
            ],
        )

    def test_count_suffix_16(self):
        self.assertEqual(
            parse("""lvs, 1 -nerved"""),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=3),
                Count(
                    start=5,
                    end=14,
                    part="leaf",
                    low=1,
                    subpart="vein",
                    trait="count",
                ),
            ],
        )

    def test_count_suffix_17(self):
        self.assertEqual(
            parse("""lvs few-nerved"""),
            [Part(part="leaf", trait="part", type="leaf_part", start=0, end=3)],
        )
