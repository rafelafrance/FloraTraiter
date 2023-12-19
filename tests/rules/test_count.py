import unittest

from flora.pylib.rules.count import Count
from flora.pylib.rules.part import Part
from flora.pylib.rules.part_location import PartLocation
from flora.pylib.rules.sex import Sex
from flora.pylib.rules.size import Dimension
from flora.pylib.rules.size import Size
from flora.pylib.rules.subpart import Subpart
from flora.pylib.rules.taxon import Taxon
from tests.setup import parse
from traiter.traiter.pylib.rules.habitat import Habitat
from traiter.traiter.pylib.rules.lat_long import LatLong


class TestCount(unittest.TestCase):
    def test_count_01(self):
        self.assertEqual(
            parse("Seeds [1–]3–12[–30]."),
            [
                Part(trait="part", part="seed", type="fruit_part", start=0, end=5),
                Count(
                    min=1,
                    low=3,
                    high=12,
                    max=30,
                    trait="count",
                    part="seed",
                    start=6,
                    end=19,
                ),
            ],
        )

    def test_count_02(self):
        self.assertEqual(
            parse("Seeds 3–12."),
            [
                Part(part="seed", trait="part", type="fruit_part", start=0, end=5),
                Count(
                    low=3,
                    high=12,
                    trait="count",
                    part="seed",
                    start=6,
                    end=10,
                ),
            ],
        )

    def test_count_03(self):
        self.assertEqual(
            parse("blade 5–10 × 4–9 cm"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=5),
                Size(
                    trait="size",
                    start=6,
                    end=19,
                    units="cm",
                    part="leaf",
                    dims=[
                        Dimension(dim="length", low=5.0, high=10.0),
                        Dimension(dim="width", low=4.0, high=9.0),
                    ],
                ),
            ],
        )

    def test_count_04(self):
        self.assertEqual(
            parse("petals 5, connate 1/2–2/3 length"),
            [
                Part(part="petal", trait="part", type="flower_part", start=0, end=6),
                Count(
                    low=5,
                    trait="count",
                    part="petal",
                    start=7,
                    end=8,
                ),
            ],
        )

    def test_count_05(self):
        self.assertEqual(
            parse("ovules mostly 120–200."),
            [
                Part(
                    part="ovary",
                    trait="part",
                    type="female_flower_part",
                    start=0,
                    end=6,
                ),
                Count(
                    low=120,
                    high=200,
                    trait="count",
                    part="ovary",
                    start=14,
                    end=21,
                ),
            ],
        )

    def test_count_06(self):
        self.assertEqual(
            parse("Staminate flowers (3–)5–10(–20)"),
            [
                Sex(
                    sex="staminate",
                    trait="sex",
                    start=0,
                    end=9,
                ),
                Part(
                    part="flower",
                    trait="part",
                    type="flower_part",
                    start=10,
                    end=17,
                    sex="staminate",
                ),
                Count(
                    min=3,
                    low=5,
                    high=10,
                    max=20,
                    trait="count",
                    start=18,
                    end=31,
                    part="flower",
                    sex="staminate",
                ),
            ],
        )

    def test_count_07(self):
        self.assertEqual(
            parse("Ovaries (4 or)5,"),
            [
                Part(
                    part="ovary",
                    trait="part",
                    type="female_flower_part",
                    start=0,
                    end=7,
                ),
                Count(
                    min=4,
                    low=5,
                    trait="count",
                    part="ovary",
                    start=8,
                    end=15,
                ),
            ],
        )

    def test_count_08(self):
        self.assertEqual(
            parse("Seeds 5(or 6)"),
            [
                Part(part="seed", trait="part", type="fruit_part", start=0, end=5),
                Count(
                    low=5,
                    max=6,
                    trait="count",
                    part="seed",
                    start=6,
                    end=13,
                ),
            ],
        )

    def test_count_09(self):
        self.assertEqual(
            parse("Seeds 5 (or 6)"),
            [
                Part(part="seed", trait="part", type="fruit_part", start=0, end=5),
                Count(
                    low=5,
                    max=6,
                    trait="count",
                    part="seed",
                    start=6,
                    end=14,
                ),
            ],
        )

    def test_count_10(self):
        self.assertEqual(
            parse("leaf (12-)23-34 × 45-56"),
            [Part(part="leaf", trait="part", type="leaf_part", start=0, end=4)],
        )

    def test_count_11(self):
        self.assertEqual(
            parse("stigma papillose on 1 side,"),
            [
                Part(
                    part="stigma",
                    trait="part",
                    type="female_flower_part",
                    start=0,
                    end=6,
                )
            ],
        )

    def test_count_12(self):
        self.assertEqual(
            parse("Male flowers with 2-8(-20) stamens;"),
            [
                Sex(
                    sex="male",
                    trait="sex",
                    start=0,
                    end=4,
                ),
                Part(
                    part="flower",
                    trait="part",
                    type="flower_part",
                    start=5,
                    end=12,
                    sex="male",
                ),
                Count(
                    low=2,
                    high=8,
                    max=20,
                    trait="count",
                    start=18,
                    end=26,
                    part="stamen",
                    sex="male",
                ),
                Part(
                    part="stamen",
                    trait="part",
                    type="male_flower_part",
                    start=27,
                    end=34,
                    sex="male",
                ),
            ],
        )

    def test_count_13(self):
        self.assertEqual(
            parse("leaflets in 3 or 4 pairs,"),
            [
                Part(part="leaflet", trait="part", type="leaf_part", start=0, end=8),
                Count(
                    low=3,
                    high=4,
                    count_group="pairs",
                    trait="count",
                    start=12,
                    end=24,
                    part="leaflet",
                ),
            ],
        )

    def test_count_14(self):
        self.assertEqual(
            parse("leaflets/lobes 11–23,"),
            [
                Part(part="leaflet", trait="part", type="leaf_part", start=0, end=8),
                Subpart(
                    subpart="lobe",
                    part="leaflet",
                    trait="subpart",
                    start=9,
                    end=14,
                ),
                Count(
                    low=11,
                    high=23,
                    trait="count",
                    part="leaflet",
                    subpart="lobe",
                    start=15,
                    end=20,
                ),
            ],
        )

    def test_count_15(self):
        self.assertEqual(
            parse("leaflets in 3 or 4(or 5) pairs,"),
            [
                Part(part="leaflet", trait="part", type="leaf_part", start=0, end=8),
                Count(
                    low=3,
                    high=4,
                    max=5,
                    count_group="pairs",
                    trait="count",
                    start=12,
                    end=30,
                    part="leaflet",
                ),
            ],
        )

    def test_count_16(self):
        self.assertEqual(
            parse("plants weigh up to 200 pounds"),
            [Part(end=6, part="plant", start=0, trait="part", type="plant_part")],
        )

    def test_count_17(self):
        self.assertEqual(
            parse("""leaf 0.5–1 times as long as opaque base."""),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=4),
                Subpart(
                    subpart="base",
                    trait="subpart",
                    start=35,
                    end=39,
                    part="leaf",
                ),
            ],
        )

    def test_count_18(self):
        self.assertEqual(
            parse("Seeds (1 or)2 or 3 per legume,"),
            [
                Part(part="seed", trait="part", type="fruit_part", start=0, end=5),
                Count(
                    min=1,
                    low=2,
                    high=3,
                    trait="count",
                    start=6,
                    end=29,
                    per_part="legume",
                    part="seed",
                ),
            ],
        )

    def test_count_19(self):
        self.assertEqual(
            parse("blade lobes 0 or 1–4(or 5) per side"),
            [
                Subpart(
                    trait="subpart",
                    start=0,
                    end=11,
                    subpart="leaf lobe",
                ),
                Count(
                    min=0,
                    low=1,
                    high=4,
                    max=5,
                    count_group="per side",
                    trait="count",
                    start=12,
                    end=35,
                    subpart="leaf lobe",
                ),
            ],
        )

    def test_count_20(self):
        self.assertEqual(
            parse("stems (11–16) pairs"),
            [
                Part(part="stem", trait="part", type="plant_part", start=0, end=5),
                Count(
                    low=11,
                    high=16,
                    trait="count",
                    start=6,
                    end=19,
                    count_group="pairs",
                    part="stem",
                ),
            ],
        )

    def test_count_21(self):
        self.assertEqual(
            parse("stamens 5–10 or 20."),
            [
                Part(
                    part="stamen",
                    trait="part",
                    type="male_flower_part",
                    start=0,
                    end=7,
                ),
                Count(
                    low=5,
                    high=10,
                    max=20,
                    trait="count",
                    part="stamen",
                    start=8,
                    end=18,
                ),
            ],
        )

    def test_count_22(self):
        self.assertEqual(
            parse("blade lobes 0 or 1–4(–9) per side"),
            [
                Subpart(trait="subpart", start=0, end=11, subpart="leaf lobe"),
                Count(
                    min=0,
                    low=1,
                    high=4,
                    max=9,
                    trait="count",
                    start=12,
                    end=33,
                    count_group="per side",
                    subpart="leaf lobe",
                ),
            ],
        )

    def test_count_23(self):
        self.assertEqual(
            parse("sepals absent;"),
            [
                Part(part="sepal", trait="part", type="flower_part", start=0, end=6),
                Count(
                    low=0,
                    trait="count",
                    part="sepal",
                    start=7,
                    end=13,
                ),
            ],
        )

    def test_count_24(self):
        self.assertEqual(
            parse("""staminate catkins in 1 or more clusters of 3--6;"""),
            [
                Sex(sex="staminate", trait="sex", start=0, end=9),
                Part(
                    part="catkin",
                    trait="part",
                    type="inflorescence",
                    start=10,
                    end=17,
                    sex="staminate",
                ),
                Count(
                    low=3,
                    high=6,
                    trait="count",
                    start=21,
                    end=47,
                    count_group="cluster",
                    part="catkin",
                    sex="staminate",
                ),
            ],
        )

    def test_count_25(self):
        self.assertEqual(
            parse("Seeds 1000"),
            [Part(end=5, part="seed", start=0, trait="part", type="fruit_part")],
        )

    def test_count_26(self):
        self.assertEqual(
            parse("""5-7(-8) free-falling article"""),
            [
                Count(
                    low=5,
                    high=7,
                    max=8,
                    trait="count",
                    start=0,
                    end=7,
                    subpart="article",
                ),
                Subpart(subpart="article", trait="subpart", start=21, end=28),
            ],
        )

    def test_count_27(self):
        self.assertEqual(
            parse("leaf of ii-iii/17-19"),
            [Part(end=4, part="leaf", start=0, trait="part", type="leaf_part")],
        )

    def test_count_28(self):
        self.assertEqual(
            parse("blades consequently imbricate 203b."),
            [Part(end=6, part="leaf", start=0, trait="part", type="leaf_part")],
        )

    def test_count_29(self):
        self.assertEqual(
            parse("bracts 84; 30,"),
            [Part(part="bract", trait="part", type="flower_part", start=0, end=6)],
        )

    def test_count_30(self):
        self.assertEqual(
            parse("stem thereon is ticketed 490d"),
            [Part(part="stem", trait="part", type="plant_part", start=0, end=4)],
        )

    def test_count_31(self):
        self.assertEqual(
            parse("septa 0;"),
            [
                Part(
                    part="septum",
                    trait="part",
                    type="female_flower_part",
                    start=0,
                    end=5,
                ),
                Count(
                    low=0,
                    trait="count",
                    start=6,
                    end=7,
                    part="septum",
                ),
            ],
        )

    def test_count_32(self):
        self.assertEqual(
            parse("lf-stk; Chihuahuan Desert 59."),
            [
                Part(part="leaf-stalk", trait="part", type="leaf_part", start=0, end=6),
                Habitat(trait="habitat", start=8, end=25, habitat="chihuahuan desert"),
            ],
        )

    def test_count_33(self):
        self.assertEqual(
            parse("""Mimosa to S. Paulo 2."""),
            [
                Taxon(
                    taxon="Mimosa",
                    rank="genus",
                    trait="taxon",
                    start=0,
                    end=6,
                    associated=True,
                )
            ],
        )

    def test_count_34(self):
        self.assertEqual(
            parse("""Mimosa lat. 13°40-14°10'S"""),
            [
                Taxon(
                    taxon="Mimosa",
                    rank="genus",
                    trait="taxon",
                    start=0,
                    end=6,
                    associated=True,
                ),
                LatLong(
                    trait="lat_long", start=12, end=25, lat_long="13° 40 -14° 10'S"
                ),
            ],
        )

    def test_count_35(self):
        self.assertEqual(
            parse("""Mimosa 18-30"""),
            [
                Taxon(
                    taxon="Mimosa",
                    rank="genus",
                    trait="taxon",
                    start=0,
                    end=6,
                    associated=True,
                )
            ],
        )

    def test_count_36(self):
        self.assertEqual(
            parse("""Pods 1-2 per capitulum,"""),
            [
                Part(part="pod", trait="part", type="fruit_part", start=0, end=4),
                Count(
                    low=1,
                    high=2,
                    trait="count",
                    start=5,
                    end=22,
                    per_part="capitulum",
                    part="pod",
                ),
            ],
        )

    def test_count_37(self):
        self.assertEqual(
            parse("""2-several times as long as corolla"""),
            [
                Part(
                    trait="part",
                    type="flower_part",
                    part="corolla",
                    start=27,
                    end=34,
                )
            ],
        )

    def test_count_38(self):
        self.assertEqual(
            parse("""the first pair 0.3-2 mm distant from unequal corolla"""),
            [
                Part(
                    part="corolla",
                    trait="part",
                    type="flower_part",
                    start=45,
                    end=52,
                )
            ],
        )

    def test_count_39(self):
        self.assertEqual(
            parse(
                """
                Pistillate flowers: hyaline bristle at apex of hypanthial
                aculei 0.5–1 times as long as opaque base."""
            ),
            [
                Sex(
                    sex="pistillate",
                    trait="sex",
                    start=0,
                    end=10,
                ),
                Part(
                    part="flower",
                    trait="part",
                    type="flower_part",
                    start=11,
                    end=18,
                    sex="pistillate",
                ),
                Subpart(
                    subpart="setae",
                    trait="subpart",
                    part_location="at apex of hypanthial aculei",
                    start=28,
                    end=35,
                    part="flower",
                ),
                PartLocation(
                    trait="part_location",
                    part_location="at apex of hypanthial aculei",
                    type="subpart_as_location",
                    start=36,
                    end=64,
                ),
                Subpart(
                    subpart="base",
                    trait="subpart",
                    part_location="at apex of hypanthial aculei",
                    start=95,
                    end=99,
                    part="flower",
                ),
            ],
        )

    def test_count_40(self):
        self.assertEqual(
            parse("Seeds (1 or)2 or 3 per legume,"),
            [
                Part(part="seed", trait="part", type="fruit_part", start=0, end=5),
                Count(
                    min=1,
                    low=2,
                    high=3,
                    trait="count",
                    start=6,
                    end=29,
                    per_part="legume",
                    part="seed",
                ),
            ],
        )

    def test_count_41(self):
        self.assertEqual(
            parse("blade lobes 0 or 1–4(or 5) per side"),
            [
                Subpart(trait="subpart", start=0, end=11, subpart="leaf lobe"),
                Count(
                    min=0,
                    low=1,
                    high=4,
                    max=5,
                    trait="count",
                    start=12,
                    end=35,
                    count_group="per side",
                    subpart="leaf lobe",
                ),
            ],
        )

    def test_count_42(self):
        self.assertEqual(
            parse("stems (11–16) pairs"),
            [
                Part(part="stem", trait="part", type="plant_part", start=0, end=5),
                Count(
                    low=11,
                    high=16,
                    count_group="pairs",
                    trait="count",
                    start=6,
                    end=19,
                    part="stem",
                ),
            ],
        )

    def test_count_43(self):
        self.assertEqual(
            parse("blade lobes 0 or 1–4(–9) per side"),
            [
                Subpart(trait="subpart", subpart="leaf lobe", start=0, end=11),
                Count(
                    min=0,
                    low=1,
                    high=4,
                    max=9,
                    trait="count",
                    start=12,
                    end=33,
                    count_group="per side",
                    subpart="leaf lobe",
                ),
            ],
        )

    def test_count_44(self):
        self.assertEqual(
            parse("sepals absent;"),
            [
                Part(part="sepal", trait="part", type="flower_part", start=0, end=6),
                Count(
                    low=0,
                    trait="count",
                    part="sepal",
                    start=7,
                    end=13,
                ),
            ],
        )

    def test_count_45(self):
        self.assertEqual(
            parse(
                """
                staminate catkins in 1 or more clusters of 3--6;
                pistillate catkins in 1 or more clusters of 2--7
                """
            ),
            [
                Sex(sex="staminate", trait="sex", start=0, end=9),
                Part(
                    part="catkin",
                    trait="part",
                    type="inflorescence",
                    start=10,
                    end=17,
                    sex="staminate",
                ),
                Count(
                    low=3,
                    high=6,
                    trait="count",
                    start=21,
                    end=47,
                    count_group="cluster",
                    part="catkin",
                    sex="staminate",
                ),
                Sex(sex="pistillate", trait="sex", start=49, end=59),
                Part(
                    part="catkin",
                    trait="part",
                    type="inflorescence",
                    start=60,
                    end=67,
                    sex="pistillate",
                ),
                Count(
                    low=2,
                    high=7,
                    trait="count",
                    start=71,
                    end=97,
                    count_group="cluster",
                    part="catkin",
                    sex="pistillate",
                ),
            ],
        )

    def test_count_46(self):
        self.assertEqual(
            parse("Seeds 1000"),
            [Part(end=5, part="seed", start=0, trait="part", type="fruit_part")],
        )

    def test_count_47(self):
        self.assertEqual(
            parse("leaves with 10 or more pinna pairs"),
            [
                Part(part="leaf", trait="part", type="leaf_part", start=0, end=6),
                Count(
                    low=10,
                    trait="count",
                    start=12,
                    end=34,
                    count_group="pairs",
                    per_part="pinna",
                    part="leaf",
                ),
            ],
        )

    def test_count_48(self):
        self.assertEqual(
            parse("(see Chapter 2 — Wood and Bark Anatomy)"),
            [Part(part="bark", trait="part", type="plant_part", start=26, end=30)],
        )

    def test_count_49(self):
        self.assertEqual(
            parse("in 1885, nos, 323 in flower"),
            [Part(end=27, part="flower", start=21, trait="part", type="flower_part")],
        )

    def test_count_50(self):
        self.assertEqual(
            parse("plant, !-17 Neto "),
            [Part(end=5, part="plant", start=0, trait="part", type="plant_part")],
        )

    def test_count_51(self):
        self.assertEqual(
            parse("plant RO-173"),
            [Part(end=5, part="plant", start=0, trait="part", type="plant_part")],
        )

    def test_count_52(self):
        self.assertEqual(
            parse("""7.5’ shrubs."""),
            [Part(end=11, part="shrub", start=5, trait="part", type="plant_part")],
        )

    def test_count_53(self):
        self.assertEqual(
            parse("""24 heads on 3-4 flowering stems;"""),
            [
                Count(
                    low=24,
                    trait="count",
                    start=0,
                    end=2,
                    part="head",
                ),
                Part(
                    trait="part",
                    type="inflorescence",
                    part="head",
                    start=3,
                    end=8,
                ),
                Count(
                    low=3,
                    high=4,
                    trait="count",
                    start=12,
                    end=15,
                    part="flowering stem",
                ),
                Part(
                    trait="part",
                    type="flower_part",
                    part="flowering stem",
                    start=16,
                    end=31,
                ),
            ],
        )
