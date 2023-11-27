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
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Shape(
                    shape="orbicular",
                    trait="shape",
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
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Shape(
                    shape="ovate-orbicular",
                    trait="shape",
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
                Part(part="petiolule", trait="part", type="leaf_part", start=0, end=9),
                Shape(
                    shape="oblanceolate",
                    trait="shape",
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
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Part(part="leaf", trait="part", type="leaf_part", start=9, end=14),
                Shape(
                    shape="ovate",
                    trait="shape",
                    part="leaf",
                    start=15,
                    end=20,
                ),
                Shape(
                    shape="orbicular",
                    trait="shape",
                    part="leaf",
                    start=24,
                    end=34,
                ),
                Shape(
                    shape="orbicular",
                    trait="shape",
                    part="leaf",
                    start=38,
                    end=51,
                ),
                Shape(
                    shape="reniform",
                    trait="shape",
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
                lanceolate-ovate or ovate-triangular,"""
            ),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Part(part="leaf", trait="part", type="leaf_part", start=8, end=13),
                Shape(
                    shape="ovate",
                    trait="shape",
                    part="leaf",
                    start=14,
                    end=19,
                ),
                Shape(
                    shape="elongate-ovate",
                    trait="shape",
                    part="leaf",
                    start=23,
                    end=37,
                ),
                Shape(
                    shape="lanceolate-ovate",
                    trait="shape",
                    part="leaf",
                    start=41,
                    end=57,
                ),
                Shape(
                    shape="ovate-triangular",
                    trait="shape",
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
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Part(part="leaf", trait="part", type="leaf_part", start=8, end=13),
                Shape(
                    shape="triangular",
                    trait="shape",
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
                broadly ovate, depressed-ovate, or reniform,"""
            ),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=2, end=7),
                Shape(
                    shape="orbicular",
                    trait="shape",
                    part="leaf",
                    start=19,
                    end=32,
                ),
                Shape(
                    shape="ovate",
                    trait="shape",
                    part="leaf",
                    start=36,
                    end=49,
                ),
                Shape(
                    shape="ovate",
                    trait="shape",
                    part="leaf",
                    start=51,
                    end=66,
                ),
                Shape(
                    shape="reniform",
                    trait="shape",
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
                reniform, shallowly to deeply palmately"""
            ),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=5),
                Shape(
                    shape="ovate-cordate",
                    trait="shape",
                    part="leaf",
                    start=6,
                    end=27,
                ),
                Shape(
                    shape="triangular-cordate",
                    trait="shape",
                    part="leaf",
                    start=31,
                    end=49,
                ),
                Shape(
                    shape="reniform",
                    trait="shape",
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
                    trait="subpart",
                    subpart="leaf lobe apex",
                    start=0,
                    end=21,
                ),
                Shape(
                    shape="orbicular",
                    trait="shape",
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
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=11),
                Shape(
                    shape="orbicular",
                    trait="shape",
                    start=12,
                    end=29,
                    part="leaf",
                ),
                Subpart(
                    subpart="lobe",
                    trait="subpart",
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
                reniform-angulate or shallowly 5-angulate."""
            ),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Part(
                    part="petiole leaf",
                    trait="part",
                    type="leaf_part",
                    start=8,
                    end=21,
                ),
                Shape(
                    shape="polygonal",
                    trait="shape",
                    start=22,
                    end=41,
                    part="petiole leaf",
                ),
                Shape(
                    shape="reniform-polygonal",
                    trait="shape",
                    start=45,
                    end=62,
                    part="petiole leaf",
                ),
                Shape(
                    shape="polygonal",
                    trait="shape",
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
                or elliptic-lanceolate,"""
            ),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=5),
                Shape(
                    shape="lanceolate",
                    trait="shape",
                    part="leaf",
                    start=6,
                    end=16,
                ),
                Shape(
                    shape="lanceolate",
                    trait="shape",
                    part="leaf",
                    start=32,
                    end=50,
                ),
                Shape(
                    shape="elliptic-lanceolate",
                    trait="shape",
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
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=5),
                Shape(
                    shape="ovate",
                    trait="shape",
                    part="leaf",
                    start=6,
                    end=19,
                ),
                Shape(
                    shape="orbicular-cordate",
                    trait="shape",
                    part="leaf",
                    start=23,
                    end=38,
                ),
                Shape(
                    shape="reniform",
                    trait="shape",
                    part="leaf",
                    start=40,
                    end=51,
                ),
                Shape(
                    shape="deltoid",
                    trait="shape",
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
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=5),
                Shape(
                    shape="orbicular",
                    trait="shape",
                    start=6,
                    end=16,
                    part="leaf",
                ),
                Shape(
                    shape="polygonal",
                    trait="shape",
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
                Part(part="petal", trait="part", type="flower_part", start=0, end=6),
                Shape(
                    shape="rhomboic-elliptic",
                    trait="shape",
                    part="petal",
                    start=16,
                    end=32,
                ),
                Shape(
                    shape="obovate",
                    trait="shape",
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
                Subpart(subpart="base", trait="subpart", start=1, end=5),
                Shape(
                    shape="truncate",
                    trait="shape",
                    subpart="base",
                    start=6,
                    end=14,
                ),
                Shape(
                    shape="cordate",
                    trait="shape",
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
                Part(part="seed", trait="part", type="fruit_part", start=0, end=5),
                Shape(
                    shape="spheric-angular",
                    trait="shape",
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
                Part(part="bract", trait="part", type="flower_part", start=0, end=9),
                Shape(
                    shape="ovate-triangular",
                    trait="shape",
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
                Part(part="petal", trait="part", type="flower_part", start=0, end=6),
                Color(
                    color="purple",
                    trait="color",
                    start=7,
                    end=13,
                    part="petal",
                ),
                Shape(
                    start=15,
                    end=23,
                    trait="shape",
                    shape="bilobate",
                    part="petal",
                ),
            ],
        )

    def test_shape_20(self):
        self.assertEqual(
            parse("blade broadly ovate-angulate to reniform-angulate"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=5),
                Shape(
                    shape="ovate-polygonal",
                    trait="shape",
                    part="leaf",
                    start=6,
                    end=28,
                ),
                Shape(
                    shape="reniform-polygonal",
                    trait="shape",
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
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Venation(
                    venation="subflabellate",
                    trait="venation",
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
                    trait="shape",
                    start=0,
                    end=16,
                    part="leaf",
                ),
                Shape(
                    shape="branched",
                    trait="shape",
                    start=20,
                    end=28,
                    part="leaf",
                ),
                Part(part="leaf", trait="part", type="leaf_part", start=29, end=34),
            ],
        )
