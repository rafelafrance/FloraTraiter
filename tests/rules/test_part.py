import unittest

from flora.pylib.rules.color import Color
from flora.pylib.rules.count import Count
from flora.pylib.rules.part import Part
from flora.pylib.rules.sex import Sex
from flora.pylib.rules.shape import Shape
from flora.pylib.rules.surface import Surface
from flora.pylib.rules.woodiness import Woodiness
from tests.setup import parse


class TestPart(unittest.TestCase):
    def test_part_01(self):
        self.assertEqual(
            parse("with thick, woody rootstock."),
            [
                Woodiness(
                    woodiness="woody",
                    part="rootstock",
                    start=12,
                    end=17,
                ),
                Part(
                    part="rootstock",
                    type="plant_part",
                    start=18,
                    end=27,
                ),
            ],
        )

    def test_part_02(self):
        self.assertEqual(
            parse("leaflets mostly 1 or 3"),
            [
                Part(part="leaflet", type="leaf_part", start=0, end=8),
                Count(
                    low=1,
                    high=3,
                    part="leaflet",
                    start=16,
                    end=22,
                ),
            ],
        )

    def test_part_03(self):
        self.assertEqual(
            parse("Receptacle discoid."),
            [
                Part(
                    part="receptacle",
                    type="flower_part",
                    start=0,
                    end=10,
                ),
                Shape(
                    shape="disk",
                    start=11,
                    end=18,
                    part="receptacle",
                ),
            ],
        )

    def test_part_04(self):
        self.assertEqual(
            parse("Flowers: sepals (pistillate)"),
            [
                Part(part="flower", type="flower_part", start=0, end=7),
                Part(
                    part="sepal",
                    type="flower_part",
                    start=9,
                    end=15,
                    sex="pistillate",
                ),
                Sex(sex="pistillate", start=16, end=28),
            ],
        )

    def test_part_05(self):
        self.assertEqual(
            parse("Flowers: staminate:"),
            [
                Part(
                    part="flower",
                    type="flower_part",
                    start=0,
                    end=7,
                ),
                Sex(
                    sex="staminate",
                    start=9,
                    end=18,
                ),
            ],
        )

    def test_part_06(self):
        self.assertEqual(
            parse("Heads more than 2-flowered"),
            [
                Part(
                    part="head",
                    type="inflorescence",
                    start=0,
                    end=5,
                ),
                Count(
                    low=2,
                    subpart="flower",
                    part="head",
                    start=16,
                    end=26,
                ),
            ],
        )

    def test_part_07(self):
        self.assertEqual(
            parse("Phyllodes glaucous"),
            [
                Part(
                    type="leaf_part",
                    start=0,
                    end=9,
                    part="phyllode",
                ),
                Color(
                    color="blue",
                    start=10,
                    end=18,
                    part="phyllode",
                ),
            ],
        )

    def test_part_08(self):
        self.assertEqual(
            parse("""stems and lf-axes hispid"""),
            [
                Part(
                    type="plant_part",
                    start=0,
                    end=17,
                    part=["stem", "leaf-axis"],
                ),
                Surface(
                    surface="hispid",
                    start=18,
                    end=24,
                    part=["stem", "leaf-axis"],
                ),
            ],
        )

    def test_part_09(self):
        self.assertEqual(
            parse("""no paraphyllidia"""),
            [
                Part(
                    end=16,
                    part="no paraphyllidia",
                    type="plant_part",
                    start=0,
                    missing=True,
                ),
            ],
        )
