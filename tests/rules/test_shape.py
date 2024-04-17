import unittest

from flora.pylib.rules.color import Color
from flora.pylib.rules.part import Part
from flora.pylib.rules.shape import Shape
from flora.pylib.rules.subpart import Subpart
from flora.pylib.rules.venation import Venation
from tests.setup import parse


class TestShape(unittest.TestCase):
    def test_shape_01(self):
        self.assertEqual(
            parse("leaf suborbiculate"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=4),
                Shape(
                    shape="orbicular",
                    part="leaf",
                    start=5,
                    end=18,
                ),
            ],
        )

    def test_shape_02(self):
        self.assertEqual(
            parse("leaf ovate-suborbicular"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=4),
                Shape(
                    shape="ovate-orbicular",
                    part="leaf",
                    start=5,
                    end=23,
                ),
            ],
        )

    def test_shape_03(self):
        self.assertEqual(
            parse("petiolule narrowly oblanceolate,"),
            [
                Part(part="petiolule", type="leaf_part", start=0, end=9),
                Shape(
                    shape="oblanceolate",
                    part="petiolule",
                    start=10,
                    end=31,
                ),
            ],
        )

    def test_shape_04(self):
        self.assertEqual(
            parse("Leaves ; blade ovate or orbiculate to suborbiculate or reniform,"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=6),
                Part(part="leaf", type="leaf_part", start=9, end=14),
                Shape(
                    shape="ovate",
                    part="leaf",
                    start=15,
                    end=20,
                ),
                Shape(
                    shape="orbicular",
                    part="leaf",
                    start=24,
                    end=34,
                ),
                Shape(
                    shape="orbicular",
                    part="leaf",
                    start=38,
                    end=51,
                ),
                Shape(
                    shape="reniform",
                    part="leaf",
                    start=55,
                    end=63,
                ),
            ],
        )

    def test_shape_05(self):
        self.assertEqual(
            parse(
                """
                Leaves: blade ovate or elongate-ovate to
                lanceolate-ovate or ovate-triangular,""",
            ),
            [
                Part(part="leaf", type="leaf_part", start=0, end=6),
                Part(part="leaf", type="leaf_part", start=8, end=13),
                Shape(
                    shape="ovate",
                    part="leaf",
                    start=14,
                    end=19,
                ),
                Shape(
                    shape="elongate-ovate",
                    part="leaf",
                    start=23,
                    end=37,
                ),
                Shape(
                    shape="lanceolate-ovate",
                    part="leaf",
                    start=41,
                    end=57,
                ),
                Shape(
                    shape="ovate-triangular",
                    part="leaf",
                    start=61,
                    end=77,
                ),
            ],
        )

    def test_shape_06(self):
        self.assertEqual(
            parse("Leaves: blade broadly to shallowly triangular"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=6),
                Part(part="leaf", type="leaf_part", start=8, end=13),
                Shape(
                    shape="triangular",
                    part="leaf",
                    start=14,
                    end=45,
                ),
            ],
        )

    def test_shape_07(self):
        self.assertEqual(
            parse(
                """
                ; blade abaxially, suborbiculate to
                broadly ovate, depressed-ovate, or reniform,""",
            ),
            [
                Part(part="leaf", type="leaf_part", start=2, end=7),
                Shape(
                    shape="orbicular",
                    part="leaf",
                    start=19,
                    end=32,
                ),
                Shape(
                    shape="ovate",
                    part="leaf",
                    start=36,
                    end=49,
                ),
                Shape(
                    shape="ovate",
                    part="leaf",
                    start=51,
                    end=66,
                ),
                Shape(
                    shape="reniform",
                    part="leaf",
                    start=71,
                    end=79,
                ),
            ],
        )

    def test_shape_08(self):
        self.assertEqual(
            parse(
                """
                blade broadly ovate-cordate to triangular-cordate or
                reniform, shallowly to deeply palmately""",
            ),
            [
                Part(part="leaf", type="leaf_part", start=0, end=5),
                Shape(
                    shape="ovate-cordate",
                    part="leaf",
                    start=6,
                    end=27,
                ),
                Shape(
                    shape="triangular-cordate",
                    part="leaf",
                    start=31,
                    end=49,
                ),
                Shape(
                    shape="reniform",
                    part="leaf",
                    start=53,
                    end=61,
                ),
            ],
        )

    def test_shape_09(self):
        self.assertEqual(
            parse("Leaf blades lobe apex rounded"),
            [
                Subpart(
                    subpart="leaf lobe apex",
                    start=0,
                    end=21,
                ),
                Shape(
                    shape="orbicular",
                    start=22,
                    end=29,
                    subpart="leaf lobe apex",
                ),
            ],
        )

    def test_shape_10(self):
        self.assertEqual(
            parse("Leaf blades mostly orbiculate, deeply to shallowly lobed,"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=11),
                Shape(
                    shape="orbicular",
                    start=12,
                    end=29,
                    part="leaf",
                ),
                Subpart(
                    subpart="lobe",
                    start=51,
                    end=56,
                    part="leaf",
                ),
            ],
        )

    def test_shape_11(self):
        self.assertEqual(
            parse(
                """
                Leaves: petiole blade pentagonal-angulate to
                reniform-angulate or shallowly 5-angulate.""",
            ),
            [
                Part(part="leaf", type="leaf_part", start=0, end=6),
                Part(
                    part="petiole leaf",
                    type="leaf_part",
                    start=8,
                    end=21,
                ),
                Shape(
                    shape="polygonal",
                    start=22,
                    end=41,
                    part="petiole leaf",
                ),
                Shape(
                    shape="reniform-polygonal",
                    start=45,
                    end=62,
                    part="petiole leaf",
                ),
                Shape(
                    shape="polygonal",
                    start=66,
                    end=86,
                    part="petiole leaf",
                ),
            ],
        )

    def test_shape_12(self):
        self.assertEqual(
            parse(
                """
                blade lanceolate to narrowly or broadly lanceolate
                or elliptic-lanceolate,""",
            ),
            [
                Part(part="leaf", type="leaf_part", start=0, end=5),
                Shape(
                    shape="lanceolate",
                    part="leaf",
                    start=6,
                    end=16,
                ),
                Shape(
                    shape="lanceolate",
                    part="leaf",
                    start=32,
                    end=50,
                ),
                Shape(
                    shape="elliptic-lanceolate",
                    part="leaf",
                    start=54,
                    end=73,
                ),
            ],
        )

    def test_shape_13(self):
        self.assertEqual(
            parse("blade broadly ovate to rounded-cordate, subreniform, or deltate"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=5),
                Shape(
                    shape="ovate",
                    part="leaf",
                    start=6,
                    end=19,
                ),
                Shape(
                    shape="orbicular-cordate",
                    part="leaf",
                    start=23,
                    end=38,
                ),
                Shape(
                    shape="reniform",
                    part="leaf",
                    start=40,
                    end=51,
                ),
                Shape(
                    shape="deltoid",
                    part="leaf",
                    start=56,
                    end=63,
                ),
            ],
        )

    def test_shape_14(self):
        self.assertEqual(
            parse("blade orbiculate to pentagonal,"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=5),
                Shape(
                    shape="orbicular",
                    start=6,
                    end=16,
                    part="leaf",
                ),
                Shape(
                    shape="polygonal",
                    start=20,
                    end=30,
                    part="leaf",
                ),
            ],
        )

    def test_shape_15(self):
        self.assertEqual(
            parse("Petals standard rhombic-elliptic to obovate,"),
            [
                Part(part="petal", type="flower_part", start=0, end=6),
                Shape(
                    shape="rhomboic-elliptic",
                    part="petal",
                    start=16,
                    end=32,
                ),
                Shape(
                    shape="obovate",
                    part="petal",
                    start=36,
                    end=43,
                ),
            ],
        )

    def test_shape_16(self):
        self.assertEqual(
            parse("<base truncate to cordate>"),
            [
                Subpart(subpart="base", start=1, end=5),
                Shape(
                    shape="truncate",
                    subpart="base",
                    start=6,
                    end=14,
                ),
                Shape(
                    shape="cordate",
                    subpart="base",
                    start=18,
                    end=25,
                ),
            ],
        )

    def test_shape_17(self):
        self.assertEqual(
            parse("Seeds globose-angular"),
            [
                Part(part="seed", type="fruit_part", start=0, end=5),
                Shape(
                    shape="spheric-angular",
                    part="seed",
                    start=6,
                    end=21,
                ),
            ],
        )

    def test_shape_18(self):
        self.assertEqual(
            parse("bractlets narrowly to broadly ovate-triangular"),
            [
                Part(part="bract", type="flower_part", start=0, end=9),
                Shape(
                    shape="ovate-triangular",
                    part="bract",
                    start=10,
                    end=46,
                ),
            ],
        )

    def test_shape_19(self):
        self.assertEqual(
            parse("Petals purple; bilobate;"),
            [
                Part(part="petal", type="flower_part", start=0, end=6),
                Color(
                    color="purple",
                    start=7,
                    end=13,
                    part="petal",
                ),
                Shape(
                    start=15,
                    end=23,
                    shape="bilobate",
                    part="petal",
                ),
            ],
        )

    def test_shape_20(self):
        self.assertEqual(
            parse("blade broadly ovate-angulate to reniform-angulate"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=5),
                Shape(
                    shape="ovate-polygonal",
                    part="leaf",
                    start=6,
                    end=28,
                ),
                Shape(
                    shape="reniform-polygonal",
                    part="leaf",
                    start=32,
                    end=49,
                ),
            ],
        )

    def test_shape_21(self):
        self.assertEqual(
            parse("leaf subflabellate"),
            [
                Part(part="leaf", type="leaf_part", start=0, end=4),
                Venation(
                    venation="subflabellate",
                    part="leaf",
                    start=5,
                    end=18,
                ),
            ],
        )

    def test_shape_22(self):
        self.assertEqual(
            parse("partly confluent or branched blade"),
            [
                Shape(
                    shape="confluent",
                    start=0,
                    end=16,
                    part="leaf",
                ),
                Shape(
                    shape="branched",
                    start=20,
                    end=28,
                    part="leaf",
                ),
                Part(part="leaf", type="leaf_part", start=29, end=34),
            ],
        )
