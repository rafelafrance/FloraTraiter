import unittest

from flora.pylib.traits.count import Count
from flora.pylib.traits.part import Part
from flora.pylib.traits.sex import Sex
from flora.pylib.traits.shape import Shape
from flora.pylib.traits.surface import Surface
from flora.pylib.traits.taxon import Taxon
from flora.pylib.traits.woodiness import Woodiness
from tests.setup import test


class TestPart(unittest.TestCase):
    def test_part_01(self):
        self.assertEqual(
            test("with thick, woody rootstock."),
            [
                Woodiness(
                    woodiness="woody",
                    trait="woodiness",
                    part="rootstock",
                    start=12,
                    end=17,
                ),
                Part(
                    part="rootstock",
                    trait="part",
                    type="plant_part",
                    start=18,
                    end=27,
                ),
            ],
        )

    def test_part_02(self):
        self.assertEqual(
            test("leaflets mostly 1 or 3"),
            [
                Part(part="leaflet", trait="part", type="leaf_part", start=0, end=8),
                Count(
                    low=1,
                    high=3,
                    trait="count",
                    part="leaflet",
                    start=16,
                    end=22,
                ),
            ],
        )

    def test_part_03(self):
        self.assertEqual(
            test("Receptacle discoid."),
            [
                Part(
                    part="receptacle",
                    trait="part",
                    type="flower_part",
                    start=0,
                    end=10,
                ),
                Shape(
                    shape="disk",
                    trait="shape",
                    start=11,
                    end=18,
                    part="receptacle",
                ),
            ],
        )

    def test_part_04(self):
        self.assertEqual(
            test("Flowers: sepals (pistillate)"),
            [
                Part(part="flower", trait="part", type="flower_part", start=0, end=7),
                Part(
                    part="sepal",
                    trait="part",
                    type="flower_part",
                    start=9,
                    end=15,
                    sex="pistillate",
                ),
                Sex(sex="pistillate", trait="sex", start=16, end=28),
            ],
        )

    def test_part_05(self):
        self.assertEqual(
            test("Flowers: staminate:"),
            [
                Part(
                    part="flower",
                    trait="part",
                    type="flower_part",
                    start=0,
                    end=7,
                ),
                Sex(
                    sex="staminate",
                    trait="sex",
                    start=9,
                    end=18,
                ),
            ],
        )

    def test_part_06(self):
        self.assertEqual(
            test("Heads more than 2-flowered"),
            [
                Part(
                    part="head",
                    trait="part",
                    type="inflorescence",
                    start=0,
                    end=5,
                ),
                Count(
                    low=2,
                    subpart="flower",
                    part="head",
                    trait="count",
                    start=16,
                    end=26,
                ),
            ],
        )

    def test_part_07(self):
        self.assertEqual(
            test("Phyllodes glaucous"),
            [
                Taxon(taxon="Phyllodes glaucous", start=0, end=9),
            ],
        )

    def test_part_08(self):
        self.maxDiff = None
        self.assertEqual(
            test("""stems and lf-axes hispid"""),
            [
                Part(
                    trait="part",
                    start=0,
                    end=17,
                    part=["stem", "leaf-axis"],
                ),
                Surface(
                    surface="hispid",
                    trait="surface",
                    start=18,
                    end=24,
                    part=["stem", "leaf-axis"],
                ),
            ],
        )

    def test_part_09(self):
        self.assertEqual(
            test("""no paraphyllidia"""),
            [
                Part(
                    end=16,
                    part="no paraphyllidia",
                    type="plant_part",
                    start=0,
                    trait="part",
                    missing=True,
                ),
            ],
        )
