import unittest

from flora.pylib.rules.color import Color
from flora.pylib.rules.count import Count
from flora.pylib.rules.margin import Margin
from flora.pylib.rules.part import Part
from flora.pylib.rules.part_location import PartLocation
from flora.pylib.rules.sex import Sex
from flora.pylib.rules.shape import Shape
from flora.pylib.rules.size import Dimension
from flora.pylib.rules.size import Size
from flora.pylib.rules.subpart import Subpart
from tests.setup import parse
from traiter.traiter.pylib.rules.elevation import Elevation
from traiter.traiter.pylib.rules.habitat import Habitat


class TestSize(unittest.TestCase):
    def test_size_01(self):
        self.assertEqual(
            parse("Leaf (12-)23-34 × 45-56 cm"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Size(
                    dims=[
                        Dimension(dim="length", min=12.0, low=23.0, high=34.0),
                        Dimension(dim="width", low=45.0, high=56.0),
                    ],
                    part="leaf",
                    trait="size",
                    start=5,
                    end=26,
                    units="cm",
                ),
            ],
        )

    def test_size_02(self):
        self.assertEqual(
            parse("leaf (12-)23-34 × 45-56"),
            [Part(part="leaf", trait="part", type="leaf_part", start=0, end=4)],
        )

    def test_size_03(self):
        self.assertEqual(
            parse("blade 1.5–5(–7) cm"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=5),
                Size(
                    dims=[Dimension(dim="length", low=1.5, high=5.0, max=7.0)],
                    trait="size",
                    start=6,
                    end=18,
                    units="cm",
                    part="leaf",
                ),
            ],
        )

    def test_size_04(self):
        self.assertEqual(
            parse("leaf shallowly to deeply 5–7-lobed"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Count(
                    low=5,
                    high=7,
                    trait="count",
                    start=25,
                    end=34,
                    part="leaf",
                    subpart="lobe",
                ),
            ],
        )

    def test_size_05(self):
        self.assertEqual(
            parse("leaf 4–10 cm wide"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Size(
                    dims=[Dimension(dim="width", low=4.0, high=10.0)],
                    trait="size",
                    start=5,
                    end=17,
                    units="cm",
                    part="leaf",
                ),
            ],
        )

    def test_size_06(self):
        self.maxDiff = None
        self.assertEqual(
            parse("leaf sinuses 1/5–1/4 to base"),
            [
                Subpart(
                    trait="subpart",
                    start=0,
                    end=12,
                    subpart="leaf sinus",
                    part_location="to base",
                ),
                PartLocation(
                    part_location="to base",
                    trait="part_location",
                    type="subpart_as_location",
                    start=21,
                    end=28,
                ),
            ],
        )

    def test_size_07(self):
        self.assertEqual(
            parse("petiolules 2–5 mm"),
            [
                Part(part="petiolule", trait="part", type="leaf_part", start=0, end=10),
                Size(
                    dims=[Dimension(dim="length", low=0.2, high=0.5)],
                    trait="size",
                    start=11,
                    end=17,
                    units="cm",
                    part="petiolule",
                ),
            ],
        )

    def test_size_08(self):
        self.assertEqual(
            parse("petiolules 2–5 mm; coarsely serrate; petioles 16–28 mm."),
            [
                Part(part="petiolule", trait="part", type="leaf_part", start=0, end=10),
                Size(
                    dims=[Dimension(dim="length", low=0.2, high=0.5)],
                    trait="size",
                    start=11,
                    end=17,
                    units="cm",
                    part="petiolule",
                ),
                Margin(
                    margin="serrate",
                    trait="margin",
                    start=19,
                    end=35,
                    part="petiolule",
                ),
                Part(part="petiole", trait="part", type="leaf_part", start=37, end=45),
                Size(
                    dims=[Dimension(dim="length", low=1.6, high=2.8)],
                    trait="size",
                    start=46,
                    end=55,
                    units="cm",
                    part="petiole",
                ),
            ],
        )

    def test_size_09(self):
        self.assertEqual(
            parse("Leaves: petiole 2–15 cm;"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Part(part="petiole", trait="part", type="leaf_part", start=8, end=15),
                Size(
                    dims=[Dimension(dim="length", low=2.0, high=15.0)],
                    trait="size",
                    start=16,
                    end=23,
                    units="cm",
                    part="petiole",
                ),
            ],
        )

    def test_size_10(self):
        self.assertEqual(
            parse("petiole [5–]7–25[–32] mm,"),
            [
                Part(part="petiole", trait="part", type="leaf_part", start=0, end=7),
                Size(
                    dims=[Dimension(dim="length", min=0.5, low=0.7, high=2.5, max=3.2)],
                    trait="size",
                    start=8,
                    end=24,
                    units="cm",
                    part="petiole",
                ),
            ],
        )

    def test_size_11(self):
        self.assertEqual(
            parse("leaf 2–4 cm × 2–10 mm"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Size(
                    dims=[
                        Dimension(dim="length", low=2.0, high=4.0),
                        Dimension(dim="width", low=0.2, high=1.0),
                    ],
                    trait="size",
                    start=5,
                    end=21,
                    part="leaf",
                    units="cm",
                ),
            ],
        )

    def test_size_12(self):
        self.assertEqual(
            parse("leaf deeply to shallowly lobed, 4–5(–7) cm wide,"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Subpart(
                    subpart="lobe",
                    trait="subpart",
                    start=25,
                    end=30,
                    part="leaf",
                ),
                Size(
                    dims=[Dimension(dim="width", low=4.0, high=5.0, max=7.0)],
                    trait="size",
                    start=32,
                    end=47,
                    units="cm",
                    part="leaf",
                    subpart="lobe",
                ),
            ],
        )

    def test_size_13(self):
        self.assertEqual(
            parse("""Leaves 3-foliolate,"""),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Count(
                    low=3,
                    trait="count",
                    start=7,
                    end=18,
                    part="leaf",
                    subpart="lobe",
                ),
            ],
        )

    def test_size_14(self):
        self.assertEqual(
            parse("terminal leaflet 3–5 cm, blade petiolule 3–12 mm,"),
            [
                PartLocation(
                    part_location="terminal",
                    trait="part_location",
                    type="part_location",
                    start=0,
                    end=8,
                ),
                Part(
                    part="leaflet",
                    trait="part",
                    type="leaf_part",
                    start=9,
                    end=16,
                    part_location="terminal",
                ),
                Size(
                    dims=[Dimension(dim="length", low=3.0, high=5.0)],
                    trait="size",
                    start=17,
                    end=23,
                    units="cm",
                    part="leaflet",
                    part_location="terminal",
                ),
                Part(
                    trait="part",
                    type="leaf_part",
                    start=25,
                    end=40,
                    part="leaf petiolule",
                ),
                Size(
                    dims=[Dimension(dim="length", low=0.3, high=1.2)],
                    trait="size",
                    units="cm",
                    start=41,
                    end=48,
                    part="leaf petiolule",
                ),
            ],
        )

    def test_size_15(self):
        self.assertEqual(
            parse("leaf shallowly 3–5(–7)-lobed, 5–25 × (8–)10–25(–30) cm,"),
            [
                Part(trait="part", type="leaf_part", part="leaf", start=0, end=4),
                Count(
                    low=3,
                    high=5,
                    max=7,
                    trait="count",
                    start=15,
                    end=28,
                    part="leaf",
                    subpart="lobe",
                ),
                Size(
                    units="cm",
                    dims=[
                        Dimension(dim="length", low=5.0, high=25.0),
                        Dimension(dim="width", min=8.0, low=10.0, high=25.0, max=30.0),
                    ],
                    trait="size",
                    start=30,
                    end=54,
                    part="leaf",
                ),
            ],
        )

    def test_size_16(self):
        self.assertEqual(
            parse("leaf (3–)5-lobed, 6–20(–30) × 6–25 cm,"),
            [
                Part(trait="part", type="leaf_part", part="leaf", start=0, end=4),
                Count(
                    min=3,
                    low=5,
                    trait="count",
                    start=5,
                    end=16,
                    part="leaf",
                    subpart="lobe",
                ),
                Size(
                    units="cm",
                    dims=[
                        Dimension(dim="length", low=6.0, high=20.0, max=30.0),
                        Dimension(dim="width", low=6.0, high=25.0),
                    ],
                    trait="size",
                    start=18,
                    end=37,
                    part="leaf",
                ),
            ],
        )

    def test_size_17(self):
        self.assertEqual(
            parse("petiole to 11 cm;"),
            [
                Part(part="petiole", trait="part", type="leaf_part", start=0, end=7),
                Size(
                    dims=[Dimension(dim="length", high=11.0)],
                    trait="size",
                    start=8,
                    end=16,
                    units="cm",
                    part="petiole",
                ),
            ],
        )

    def test_size_18(self):
        self.assertEqual(
            parse("petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate)"),
            [
                Part(
                    part="petal",
                    trait="part",
                    type="flower_part",
                    start=0,
                    end=6,
                ),
                Size(
                    dims=[Dimension(dim="length", min=0.1, low=0.3, high=1.0, max=1.2)],
                    sex="pistillate",
                    trait="size",
                    start=7,
                    end=36,
                    units="cm",
                    part="petal",
                ),
                Size(
                    dims=[Dimension(dim="length", low=0.5, high=0.8, max=1.0)],
                    sex="staminate",
                    trait="size",
                    start=40,
                    end=63,
                    units="cm",
                    part="petal",
                ),
            ],
        )

    def test_size_19(self):
        self.assertEqual(
            parse("Flowers 5–10 cm diam.; hypanthium 4–8 mm,"),
            [
                Part(part="flower", trait="part", type="flower_part", start=0, end=7),
                Size(
                    dims=[Dimension(dim="diameter", low=5.0, high=10.0)],
                    trait="size",
                    start=8,
                    end=21,
                    units="cm",
                    part="flower",
                ),
                Part(
                    trait="part",
                    part="hypanthium",
                    type="flower_part",
                    start=23,
                    end=33,
                ),
                Size(
                    dims=[Dimension(dim="length", low=0.4, high=0.8)],
                    trait="size",
                    start=34,
                    end=40,
                    units="cm",
                    part="hypanthium",
                ),
            ],
        )

    def test_size_20(self):
        self.assertEqual(
            parse("Flowers 5--16 × 4--12 cm"),
            [
                Part(part="flower", trait="part", type="flower_part", start=0, end=7),
                Size(
                    dims=[
                        Dimension(dim="length", low=5.0, high=16.0),
                        Dimension(dim="width", low=4.0, high=12.0),
                    ],
                    trait="size",
                    start=8,
                    end=24,
                    part="flower",
                    units="cm",
                ),
            ],
        )

    def test_size_21(self):
        self.assertEqual(
            parse(
                """
                Inflorescences formed season before flowering and exposed
                during winter; staminate catkins 3--8.5 cm,"""
            ),
            [
                Part(
                    part="inflorescence",
                    trait="part",
                    type="inflorescence",
                    start=0,
                    end=14,
                ),
                Sex(sex="staminate", trait="sex", start=73, end=82),
                Part(
                    part="catkin",
                    trait="part",
                    type="inflorescence",
                    start=83,
                    end=90,
                    sex="staminate",
                ),
                Size(
                    dims=[Dimension(dim="length", low=3.0, high=8.5)],
                    trait="size",
                    start=91,
                    end=100,
                    part="catkin",
                    sex="staminate",
                    units="cm",
                ),
            ],
        )

    def test_size_22(self):
        self.assertEqual(
            parse("Leaflets petiolulate; blade ovate, 8-15 × 4-15 cm,"),
            [
                Part(part="leaflet", trait="part", type="leaf_part", start=0, end=8),
                Part(part="leaf", trait="part", type="leaf_part", start=22, end=27),
                Shape(
                    shape="ovate",
                    trait="shape",
                    start=28,
                    end=33,
                    part="leaf",
                ),
                Size(
                    dims=[
                        Dimension(dim="length", low=8.0, high=15.0),
                        Dimension(dim="width", low=4.0, high=15.0),
                    ],
                    trait="size",
                    start=35,
                    end=49,
                    part="leaf",
                    units="cm",
                ),
            ],
        )

    def test_size_23(self):
        self.assertEqual(
            parse("calyx, 8-10 mm, 3-4 mm high,"),
            [
                Part(part="calyx", trait="part", type="flower_part", start=0, end=5),
                Size(
                    dims=[
                        Dimension(dim="length", low=0.8, high=1.0),
                        Dimension(dim="height", low=0.3, high=0.4),
                    ],
                    trait="size",
                    start=7,
                    end=27,
                    part="calyx",
                    units="cm",
                ),
            ],
        )

    def test_size_24(self):
        self.assertEqual(
            parse("Petals 15-21 × ca. 8 mm,"),
            [
                Part(part="petal", trait="part", type="flower_part", start=0, end=6),
                Size(
                    dims=[
                        Dimension(dim="length", low=1.5, high=2.1),
                        Dimension(dim="width", low=0.8),
                    ],
                    trait="size",
                    start=7,
                    end=23,
                    part="petal",
                    uncertain=True,
                    units="cm",
                ),
            ],
        )

    def test_size_25(self):
        self.assertEqual(
            parse("Petals ca 8 mm."),
            [
                Part(part="petal", trait="part", type="flower_part", start=0, end=6),
                Size(
                    dims=[Dimension(dim="length", low=0.8)],
                    trait="size",
                    start=7,
                    end=15,
                    part="petal",
                    uncertain=True,
                    units="cm",
                ),
            ],
        )

    def test_size_26(self):
        self.assertEqual(
            parse("Legumes 7-10 mm, 2.8-4.5 mm high and wide"),
            [
                Part(part="legume", trait="part", type="fruit_part", start=0, end=7),
                Size(
                    dims=[
                        Dimension(dim="height", low=0.7, high=1.0),
                        Dimension(dim="width", low=0.28, high=0.45),
                    ],
                    trait="size",
                    start=8,
                    end=41,
                    part="legume",
                    units="cm",
                ),
            ],
        )

    def test_size_27(self):
        self.assertEqual(
            parse("Racemes 3-4 cm,"),
            [
                Part(
                    part="raceme",
                    trait="part",
                    type="inflorescence",
                    start=0,
                    end=7,
                ),
                Size(
                    dims=[Dimension(dim="length", low=3.0, high=4.0)],
                    trait="size",
                    start=8,
                    end=14,
                    part="raceme",
                    units="cm",
                ),
            ],
        )

    def test_size_28(self):
        self.assertEqual(
            parse(
                "Petals pale violet, with darker keel; standard elliptic, 6-7 × 3-4;"
            ),
            [
                Part(part="petal", trait="part", type="flower_part", start=0, end=6),
                Color(
                    color="purple",
                    trait="color",
                    start=7,
                    end=18,
                    part="petal",
                ),
                Part(
                    part="keel",
                    trait="part",
                    type="flower_part",
                    start=32,
                    end=36,
                ),
                Shape(
                    shape="elliptic",
                    trait="shape",
                    start=47,
                    end=55,
                    part="keel",
                ),
            ],
        )

    def test_size_29(self):
        self.assertEqual(
            parse("Seeds ca. 1.6 × 1-1.3 × 0.7-0.8 cm; hilum 8-10 mm."),
            [
                Part(part="seed", trait="part", type="fruit_part", start=0, end=5),
                Size(
                    dims=[
                        Dimension(dim="length", low=1.6),
                        Dimension(dim="width", low=1.0, high=1.3),
                        Dimension(dim="thickness", low=0.7, high=0.8),
                    ],
                    trait="size",
                    start=6,
                    end=34,
                    uncertain=True,
                    part="seed",
                    units="cm",
                ),
                Part(part="hilum", trait="part", type="fruit_part", start=36, end=41),
                Size(
                    dims=[Dimension(dim="length", low=0.8, high=1.0)],
                    trait="size",
                    start=42,
                    end=50,
                    part="hilum",
                    units="cm",
                ),
            ],
        )

    def test_size_30(self):
        self.assertEqual(
            parse("leaflets obovate, 1-2.5 × to 1.6 cm,"),
            [
                Part(part="leaflet", trait="part", type="leaf_part", start=0, end=8),
                Shape(
                    shape="obovate",
                    trait="shape",
                    start=9,
                    end=16,
                    part="leaflet",
                ),
                Size(
                    dims=[
                        Dimension(dim="length", low=1.0, high=2.5),
                        Dimension(dim="width", low=1.6),
                    ],
                    trait="size",
                    start=18,
                    end=35,
                    part="leaflet",
                    units="cm",
                ),
            ],
        )

    def test_size_31(self):
        self.assertEqual(
            parse("Shrubs, 0.5–1[–2.5] m."),
            [
                Part(part="shrub", trait="part", type="plant_part", start=0, end=6),
                Size(
                    dims=[Dimension(dim="length", low=50.0, high=100.0, max=250.0)],
                    trait="size",
                    part="shrub",
                    start=8,
                    end=22,
                    units="cm",
                ),
            ],
        )

    def test_size_32(self):
        self.assertEqual(
            parse("trunk to 3(?) cm d.b.h.;"),
            [
                Part(part="trunk", trait="part", type="plant_part", start=0, end=5),
                Size(
                    dims=[Dimension(dim="dbh", high=3.0)],
                    uncertain=True,
                    trait="size",
                    start=6,
                    end=23,
                    part="trunk",
                    units="cm",
                ),
            ],
        )

    def test_size_33(self):
        self.assertEqual(
            parse("Trees to 25 m tall; bark yellow-brown, fissured."),
            [
                Part(part="tree", trait="part", type="plant_part", start=0, end=5),
                Size(
                    dims=[Dimension(dim="height", high=2500.0)],
                    trait="size",
                    start=6,
                    end=18,
                    part="tree",
                    units="cm",
                ),
                Part(part="bark", trait="part", type="plant_part", start=20, end=24),
                Color(
                    color="yellow-brown",
                    trait="color",
                    start=25,
                    end=37,
                    part="bark",
                ),
            ],
        )

    def test_size_34(self):
        self.assertEqual(
            parse("Shrubs or trees , 3-50 m. Bark light to dark gray"),
            [
                Part(part="shrub", trait="part", type="plant_part", start=0, end=6),
                Part(part="tree", trait="part", type="plant_part", start=10, end=15),
                Size(
                    dims=[Dimension(dim="length", low=300.0, high=5000.0)],
                    trait="size",
                    start=18,
                    end=25,
                    part="bark",
                    units="cm",
                ),
                Part(part="bark", trait="part", type="plant_part", start=26, end=30),
                Color(
                    color="gray",
                    trait="color",
                    start=40,
                    end=49,
                    part="bark",
                ),
            ],
        )

    def test_size_35(self):
        self.assertEqual(
            parse("Leaves (2-)3-5 mm ."),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Size(
                    dims=[Dimension(dim="length", min=0.2, low=0.3, high=0.5)],
                    trait="size",
                    start=7,
                    end=19,
                    part="leaf",
                    units="cm",
                ),
            ],
        )

    def test_size_36(self):
        self.assertEqual(
            parse("articles ±4.5 mm long;"),
            [
                Subpart(subpart="article", trait="subpart", start=0, end=8),
                Size(
                    dims=[Dimension(dim="length", low=0.45)],
                    trait="size",
                    start=9,
                    end=21,
                    uncertain=True,
                    subpart="article",
                    units="cm",
                ),
            ],
        )

    def test_size_37(self):
        self.assertEqual(
            parse("seeds ± 4 x 3 mm."),
            [
                Part(part="seed", trait="part", type="fruit_part", start=0, end=5),
                Size(
                    dims=[
                        Dimension(dim="length", low=0.4),
                        Dimension(dim="width", low=0.3),
                    ],
                    trait="size",
                    start=6,
                    end=17,
                    uncertain=True,
                    part="seed",
                    units="cm",
                ),
            ],
        )

    def test_size_38(self):
        self.assertEqual(
            parse("coastal plain to 1500 m,"),
            [Habitat(trait="habitat", start=8, end=13, habitat="plain")],
        )

    def test_size_39(self):
        self.assertEqual(
            parse("trunk to 8(-?) cm diam."),
            [
                Part(part="trunk", trait="part", type="plant_part", start=0, end=5),
                Size(
                    dims=[Dimension(dim="diameter", low=8.0)],
                    trait="size",
                    start=9,
                    end=23,
                    uncertain=True,
                    part="trunk",
                    units="cm",
                ),
            ],
        )

    def test_size_40(self):
        self.assertEqual(
            parse(
                """setae to 2-6 mm and to 0.4-0.7 mm diam. at base, these mixed with
                non-secretory setulae"""
            ),
            [
                Part(part="setae", trait="part", type="plant_part", start=0, end=5),
                Size(
                    dims=[Dimension(dim="length", low=0.2, high=0.6)],
                    trait="size",
                    start=9,
                    end=15,
                    part="setae",
                    units="cm",
                ),
                Size(
                    dims=[Dimension(dim="diameter", low=0.04, high=0.07)],
                    trait="size",
                    start=23,
                    end=39,
                    part="setae",
                    part_location="at base",
                    units="cm",
                ),
                PartLocation(
                    part_location="at base",
                    type="subpart_as_location",
                    trait="part_location",
                    start=40,
                    end=47,
                ),
                Part(
                    part="setulae",
                    trait="part",
                    type="plant_part",
                    start=80,
                    end=87,
                ),
            ],
        )

    def test_size_41(self):
        self.assertEqual(
            parse("""setae (3.5-)4-7 x (1.5_)2- 2.8 mm"""),
            [
                Part(part="setae", trait="part", type="plant_part", start=0, end=5),
                Size(
                    dims=[
                        Dimension(dim="length", min=0.35, low=0.4, high=0.7),
                        Dimension(dim="width", min=0.15, low=0.2, high=0.28),
                    ],
                    trait="size",
                    start=6,
                    end=33,
                    part="setae",
                    units="cm",
                ),
            ],
        )

    def test_size_42(self):
        self.assertEqual(
            parse(""" flowers: 7 ft tall; """),
            [
                Part(part="flower", trait="part", type="flower_part", start=0, end=7),
                Size(
                    dims=[Dimension(dim="height", low=213.36)],
                    trait="size",
                    start=9,
                    end=18,
                    part="flower",
                    units="cm",
                ),
            ],
        )

    def test_size_43(self):
        self.assertEqual(
            parse("""Tree Cc. 650 m;"""),
            [
                Part(part="tree", trait="part", type="plant_part", start=0, end=4),
                Elevation(
                    trait="elevation", elevation=650.0, units="m", start=5, end=14
                ),
            ],
        )

    def test_size_44(self):
        self.assertEqual(
            parse(
                """
                flowers: 7
                ft tall;
                """
            ),
            [
                Part(type="flower_part", trait="part", part="flower", start=0, end=7),
                Size(
                    units="cm",
                    dims=[Dimension(dim="height", low=213.36)],
                    trait="size",
                    start=9,
                    end=18,
                    part="flower",
                ),
            ],
        )
