import unittest

from flora.pylib.traits.part import Part
from flora.pylib.traits.plant_location import PlantLocation
from flora.pylib.traits.shape import Shape
from flora.pylib.traits.size import Dimension
from flora.pylib.traits.size import Size
from flora.pylib.traits.surface import Surface
from tests.setup import test


class TestPartLocation(unittest.TestCase):
    def test_part_location_01(self):
        self.assertEqual(
            test("stipules 3-8 mm, semiamplexicaul, adnate to petiole for 1-2 mm"),
            [
                Part(part="stipule", trait="part", type="leaf_part", start=0, end=8),
                Size(
                    dims=[Dimension("length", low=0.3, high=0.8)],
                    trait="size",
                    start=9,
                    end=15,
                    units="cm",
                    part="stipule",
                ),
                Shape(
                    shape="semiamplexicaul",
                    trait="shape",
                    start=17,
                    end=32,
                    part="stipule",
                ),
                PlantLocation(
                    location="adnate to petiole for 1 - 2 mm",
                    trait="location",
                    type="part_as_distance",
                    start=34,
                    end=62,
                ),
            ],
        )

    def test_part_location_02(self):
        self.assertEqual(
            test("leaves completely embracing stem but not connate"),
            [
                Part(
                    part="leaf",
                    trait="part",
                    type="leaf_part",
                    start=0,
                    end=6,
                    location="embracing stem",
                ),
                PlantLocation(
                    location="embracing stem",
                    trait="location",
                    type="part_as_location",
                    start=18,
                    end=32,
                ),
            ],
        )

    def test_part_location_03(self):
        self.assertEqual(
            test("stipules shortly ciliate at margin"),
            [
                Part(
                    part="stipule",
                    trait="part",
                    type="leaf_part",
                    location="at margin",
                    start=0,
                    end=8,
                ),
                Surface(
                    surface="ciliate",
                    trait="surface",
                    location="at margin",
                    start=9,
                    end=24,
                    part="stipule",
                ),
                PlantLocation(
                    location="at margin",
                    trait="location",
                    type="subpart_as_location",
                    start=25,
                    end=34,
                ),
            ],
        )

    def test_part_location_04(self):
        self.assertEqual(
            test("capitula immersed in foliage."),
            [
                Part(
                    part="capitulum",
                    trait="part",
                    type="inflorescence",
                    location="immersed in foliage",
                    start=0,
                    end=8,
                ),
                PlantLocation(
                    location="immersed in foliage",
                    trait="location",
                    type="part_as_location",
                    start=9,
                    end=28,
                ),
            ],
        )

    def test_part_location_05(self):
        self.maxDiff = None
        self.assertEqual(
            test(
                "the short terminal pseudoraceme of ovoid-ellipsoid or globose "
                "capitula immersed in foliage."
            ),
            [
                PlantLocation(
                    trait="location",
                    start=10,
                    end=18,
                    location="terminal",
                    type="part_location",
                ),
                Part(
                    part="pseudoraceme",
                    trait="part",
                    type="inflorescence",
                    start=19,
                    end=31,
                    location="terminal",
                ),
                Shape(
                    shape="ovoid-ellipsoid",
                    trait="shape",
                    start=35,
                    end=50,
                    part="pseudoraceme",
                    location="terminal",
                ),
                Shape(
                    shape="spheric",
                    trait="shape",
                    start=54,
                    end=61,
                    part="capitulum",
                    location="immersed in foliage",
                ),
                Part(
                    part="capitulum",
                    trait="part",
                    type="inflorescence",
                    start=62,
                    end=70,
                    location="immersed in foliage",
                ),
                PlantLocation(
                    location="immersed in foliage",
                    trait="location",
                    type="part_as_location",
                    start=71,
                    end=90,
                ),
            ],
        )

    def test_part_location_06(self):
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
                PlantLocation(
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
