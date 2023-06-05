import unittest

from tests.setup import test


class TestCount(unittest.TestCase):
    def test_count_01(self):
        self.assertEqual(
            test("Seeds [1–]3–12[–30]."),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "min": 1,
                    "low": 3,
                    "high": 12,
                    "max": 30,
                    "trait": "count",
                    "fruit_part": "seed",
                    "start": 6,
                    "end": 19,
                },
            ],
        )

    def test_count_02(self):
        self.assertEqual(
            test("Seeds 3–12."),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "low": 3,
                    "high": 12,
                    "trait": "count",
                    "fruit_part": "seed",
                    "start": 6,
                    "end": 10,
                },
            ],
        )

    def test_count_03(self):
        self.assertEqual(
            test("blade 5–10 × 4–9 cm"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 5},
                {
                    "dimensions": ["length", "width"],
                    "length_low": 5.0,
                    "length_high": 10.0,
                    "trait": "size",
                    "start": 6,
                    "end": 19,
                    "leaf_part": "leaf",
                    "width_low": 4.0,
                    "width_high": 9.0,
                    "units": "cm",
                },
            ],
        )

    def test_count_04(self):
        self.assertEqual(
            test("petals 5, connate 1/2–2/3 length"),
            [
                {"flower_part": "petal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "low": 5,
                    "trait": "count",
                    "flower_part": "petal",
                    "start": 7,
                    "end": 8,
                },
            ],
        )

    def test_count_05(self):
        self.assertEqual(
            test("ovules mostly 120–200."),
            [
                {
                    "female_flower_part": "ovary",
                    "trait": "female_flower_part",
                    "start": 0,
                    "end": 6,
                },
                {
                    "low": 120,
                    "high": 200,
                    "trait": "count",
                    "female_flower_part": "ovary",
                    "start": 14,
                    "end": 21,
                },
            ],
        )

    def test_count_06(self):
        self.assertEqual(
            test("Staminate flowers (3–)5–10(–20)"),
            [
                {
                    "sex": "staminate",
                    "trait": "sex",
                    "start": 0,
                    "end": 9,
                },
                {
                    "flower_part": "flower",
                    "trait": "flower_part",
                    "start": 10,
                    "end": 17,
                    "sex": "staminate",
                },
                {
                    "min": 3,
                    "low": 5,
                    "high": 10,
                    "max": 20,
                    "trait": "count",
                    "start": 18,
                    "end": 31,
                    "flower_part": "flower",
                    "sex": "staminate",
                },
            ],
        )

    def test_count_07(self):
        self.assertEqual(
            test("Ovaries (4 or)5,"),
            [
                {
                    "female_flower_part": "ovary",
                    "trait": "female_flower_part",
                    "start": 0,
                    "end": 7,
                },
                {
                    "min": 4,
                    "low": 5,
                    "trait": "count",
                    "female_flower_part": "ovary",
                    "start": 8,
                    "end": 15,
                },
            ],
        )

    def test_count_08(self):
        self.assertEqual(
            test("Seeds 5(or 6)"),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "low": 5,
                    "max": 6,
                    "trait": "count",
                    "fruit_part": "seed",
                    "start": 6,
                    "end": 13,
                },
            ],
        )

    def test_count_09(self):
        self.assertEqual(
            test("Seeds 5 (or 6)"),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "low": 5,
                    "max": 6,
                    "trait": "count",
                    "fruit_part": "seed",
                    "start": 6,
                    "end": 14,
                },
            ],
        )

    def test_count_10(self):
        self.assertEqual(
            test("leaf (12-)23-34 × 45-56"),
            [{"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4}],
        )

    def test_count_11(self):
        self.assertEqual(
            test("stigma papillose on 1 side,"),
            [
                {
                    "female_flower_part": "stigma",
                    "trait": "female_flower_part",
                    "start": 0,
                    "end": 6,
                }
            ],
        )

    def test_count_12(self):
        self.assertEqual(
            test("Male flowers with 2-8(-20) stamens;"),
            [
                {
                    "sex": "male",
                    "trait": "sex",
                    "start": 0,
                    "end": 4,
                },
                {
                    "flower_part": "flower",
                    "trait": "flower_part",
                    "start": 5,
                    "end": 12,
                    "sex": "male",
                },
                {
                    "low": 2,
                    "high": 8,
                    "max": 20,
                    "trait": "count",
                    "start": 18,
                    "end": 26,
                    "male_flower_part": "stamen",
                    "sex": "male",
                },
                {
                    "male_flower_part": "stamen",
                    "trait": "male_flower_part",
                    "start": 27,
                    "end": 34,
                    "sex": "male",
                },
            ],
        )

    def test_count_13(self):
        self.assertEqual(
            test("leaflets in 3 or 4 pairs,"),
            [
                {"leaf_part": "leaflet", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "low": 3,
                    "high": 4,
                    "count_group": "pairs",
                    "trait": "count",
                    "start": 12,
                    "end": 24,
                    "leaf_part": "leaflet",
                },
            ],
        )

    def test_count_14(self):
        self.assertEqual(
            test("leaflets/lobes 11–23,"),
            [
                {"leaf_part": "leaflet", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "subpart": "lobe",
                    "leaf_part": "leaflet",
                    "trait": "subpart",
                    "start": 9,
                    "end": 14,
                },
                {
                    "low": 11,
                    "high": 23,
                    "trait": "count",
                    "leaf_part": "leaflet",
                    "subpart": "lobe",
                    "start": 15,
                    "end": 20,
                },
            ],
        )

    def test_count_15(self):
        self.assertEqual(
            test("leaflets in 3 or 4(or 5) pairs,"),
            [
                {"leaf_part": "leaflet", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "low": 3,
                    "high": 4,
                    "max": 5,
                    "count_group": "pairs",
                    "trait": "count",
                    "start": 12,
                    "end": 30,
                    "leaf_part": "leaflet",
                },
            ],
        )

    def test_count_16(self):
        self.assertEqual(
            test("plants weigh up to 200 pounds"),
            [{"end": 6, "plant_part": "plant", "start": 0, "trait": "plant_part"}],
        )

    def test_count_17(self):
        self.assertEqual(
            test("""leaf 0.5–1 times as long as opaque base."""),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 4},
                {
                    "subpart": "base",
                    "trait": "subpart",
                    "start": 35,
                    "end": 39,
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_count_18(self):
        self.assertEqual(
            test("Seeds (1 or)2 or 3 per legume,"),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "min": 1,
                    "low": 2,
                    "high": 3,
                    "trait": "count",
                    "start": 6,
                    "end": 29,
                    "per_part": "legume",
                    "fruit_part": "seed",
                },
            ],
        )

    def test_count_19(self):
        self.assertEqual(
            test("blade lobes 0 or 1–4(or 5) per side"),
            [
                {
                    "trait": "subpart",
                    "start": 0,
                    "end": 11,
                    "subpart": "leaf lobe",
                },
                {
                    "min": 0,
                    "low": 1,
                    "high": 4,
                    "max": 5,
                    "count_group": "per side",
                    "trait": "count",
                    "start": 12,
                    "end": 35,
                    "subpart": "leaf lobe",
                },
            ],
        )

    def test_count_20(self):
        self.assertEqual(
            test("stems (11–16) pairs"),
            [
                {"plant_part": "stem", "trait": "plant_part", "start": 0, "end": 5},
                {
                    "low": 11,
                    "high": 16,
                    "trait": "count",
                    "start": 6,
                    "end": 19,
                    "count_group": "pairs",
                    "plant_part": "stem",
                },
            ],
        )

    def test_count_21(self):
        self.assertEqual(
            test("stamens 5–10 or 20."),
            [
                {
                    "male_flower_part": "stamen",
                    "trait": "male_flower_part",
                    "start": 0,
                    "end": 7,
                },
                {
                    "low": 5,
                    "high": 10,
                    "max": 20,
                    "trait": "count",
                    "male_flower_part": "stamen",
                    "start": 8,
                    "end": 18,
                },
            ],
        )

    def test_count_22(self):
        self.assertEqual(
            test("blade lobes 0 or 1–4(–9) per side"),
            [
                {"trait": "subpart", "start": 0, "end": 11, "subpart": "leaf lobe"},
                {
                    "min": 0,
                    "low": 1,
                    "high": 4,
                    "max": 9,
                    "trait": "count",
                    "start": 12,
                    "end": 33,
                    "count_group": "per side",
                    "subpart": "leaf lobe",
                },
            ],
        )

    def test_count_23(self):
        self.assertEqual(
            test("sepals absent;"),
            [
                {"flower_part": "sepal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "low": 0,
                    "trait": "count",
                    "flower_part": "sepal",
                    "start": 7,
                    "end": 13,
                },
            ],
        )

    def test_count_24(self):
        self.assertEqual(
            test("""staminate catkins in 1 or more clusters of 3--6;"""),
            [
                {"sex": "staminate", "trait": "sex", "start": 0, "end": 9},
                {
                    "inflorescence": "catkin",
                    "trait": "inflorescence",
                    "start": 10,
                    "end": 17,
                    "sex": "staminate",
                },
                {
                    "low": 3,
                    "high": 6,
                    "trait": "count",
                    "start": 21,
                    "end": 47,
                    "count_group": "cluster",
                    "inflorescence": "catkin",
                    "sex": "staminate",
                },
            ],
        )

    def test_count_25(self):
        self.assertEqual(
            test("Seeds 1000"),
            [{"end": 5, "fruit_part": "seed", "start": 0, "trait": "fruit_part"}],
        )

    def test_count_26(self):
        self.assertEqual(
            test("""5-7(-8) free-falling article"""),
            [
                {
                    "low": 5,
                    "high": 7,
                    "max": 8,
                    "trait": "count",
                    "start": 0,
                    "end": 7,
                    "subpart": "article",
                },
                {"subpart": "article", "trait": "subpart", "start": 21, "end": 28},
            ],
        )

    def test_count_27(self):
        self.assertEqual(
            test("leaf of ii-iii/17-19"),
            [{"end": 4, "leaf_part": "leaf", "start": 0, "trait": "leaf_part"}],
        )

    def test_count_28(self):
        self.assertEqual(
            test("blades consequently imbricate 203b."),
            [{"end": 6, "leaf_part": "leaf", "start": 0, "trait": "leaf_part"}],
        )

    def test_count_29(self):
        self.assertEqual(
            test("bracts 84; 30,"),
            [{"leaf_part": "bract", "trait": "leaf_part", "start": 0, "end": 6}],
        )

    def test_count_30(self):
        self.assertEqual(
            test("stem thereon is ticketed 490d"),
            [{"plant_part": "stem", "trait": "plant_part", "start": 0, "end": 4}],
        )

    def test_count_31(self):
        self.assertEqual(
            test("septa 0;"),
            [
                {
                    "female_flower_part": "septum",
                    "trait": "female_flower_part",
                    "start": 0,
                    "end": 5,
                },
                {
                    "low": 0,
                    "trait": "count",
                    "start": 6,
                    "end": 7,
                    "female_flower_part": "septum",
                },
            ],
        )

    def test_count_32(self):
        self.assertEqual(
            test("lf-stk; Chihuahuan Desert 59."),
            [{"leaf_part": "leaf-stalk", "trait": "leaf_part", "start": 0, "end": 6}],
        )

    def test_count_33(self):
        self.assertEqual(
            test("""Mimosa to S. Paulo 2."""),
            [
                {
                    "taxon": "Mimosa",
                    "rank": "genus",
                    "trait": "taxon",
                    "start": 0,
                    "end": 6,
                }
            ],
        )

    def test_count_34(self):
        self.assertEqual(
            test("""Mimosa lat. 13°40-14°10'S"""),
            [
                {
                    "taxon": "Mimosa",
                    "rank": "genus",
                    "trait": "taxon",
                    "start": 0,
                    "end": 6,
                }
            ],
        )

    def test_count_35(self):
        self.assertEqual(
            test("""Mimosa 18-30"""),
            [
                {
                    "taxon": "Mimosa",
                    "rank": "genus",
                    "trait": "taxon",
                    "start": 0,
                    "end": 6,
                }
            ],
        )

    def test_count_36(self):
        self.assertEqual(
            test("""Pods 1-2 per capitulum,"""),
            [
                {"fruit_part": "pod", "trait": "fruit_part", "start": 0, "end": 4},
                {
                    "low": 1,
                    "high": 2,
                    "trait": "count",
                    "start": 5,
                    "end": 22,
                    "per_part": "capitulum",
                    "fruit_part": "pod",
                },
            ],
        )

    def test_count_37(self):
        self.assertEqual(
            test("""2-several times as long as corolla"""),
            [
                {
                    "trait": "flower_part",
                    "flower_part": "corolla",
                    "start": 27,
                    "end": 34,
                }
            ],
        )

    def test_count_38(self):
        self.assertEqual(
            test("""the first pair 0.3-2 mm distant from unequal corolla"""),
            [
                {
                    "flower_part": "corolla",
                    "trait": "flower_part",
                    "start": 45,
                    "end": 52,
                }
            ],
        )

    def test_count_39(self):
        self.assertEqual(
            test(
                """
                Pistillate flowers: hyaline bristle at apex of hypanthial
                aculei 0.5–1 times as long as opaque base."""
            ),
            [
                {
                    "sex": "pistillate",
                    "trait": "sex",
                    "start": 0,
                    "end": 10,
                },
                {
                    "flower_part": "flower",
                    "trait": "flower_part",
                    "start": 11,
                    "end": 18,
                    "sex": "pistillate",
                },
                {
                    "subpart": "setae",
                    "trait": "subpart",
                    "start": 28,
                    "end": 35,
                    "flower_part": "flower",
                },
                {
                    "subpart_as_loc": "at apex of hypanthial aculei",
                    "trait": "subpart_as_loc",
                    "start": 36,
                    "end": 64,
                },
                {
                    "subpart": "base",
                    "trait": "subpart",
                    "start": 95,
                    "end": 99,
                    "flower_part": "flower",
                },
            ],
        )

    def test_count_40(self):
        self.assertEqual(
            test("Seeds (1 or)2 or 3 per legume,"),
            [
                {"fruit_part": "seed", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "min": 1,
                    "low": 2,
                    "high": 3,
                    "trait": "count",
                    "start": 6,
                    "end": 29,
                    "per_part": "legume",
                    "fruit_part": "seed",
                },
            ],
        )

    def test_count_41(self):
        self.assertEqual(
            test("blade lobes 0 or 1–4(or 5) per side"),
            [
                {"trait": "subpart", "start": 0, "end": 11, "subpart": "leaf lobe"},
                {
                    "min": 0,
                    "low": 1,
                    "high": 4,
                    "max": 5,
                    "trait": "count",
                    "start": 12,
                    "end": 35,
                    "count_group": "per side",
                    "subpart": "leaf lobe",
                },
            ],
        )

    def test_count_42(self):
        self.assertEqual(
            test("stems (11–16) pairs"),
            [
                {"plant_part": "stem", "trait": "plant_part", "start": 0, "end": 5},
                {
                    "low": 11,
                    "high": 16,
                    "count_group": "pairs",
                    "trait": "count",
                    "start": 6,
                    "end": 19,
                    "plant_part": "stem",
                },
            ],
        )

    def test_count_43(self):
        self.assertEqual(
            test("blade lobes 0 or 1–4(–9) per side"),
            [
                {"trait": "subpart", "subpart": "leaf lobe", "start": 0, "end": 11},
                {
                    "min": 0,
                    "low": 1,
                    "high": 4,
                    "max": 9,
                    "trait": "count",
                    "start": 12,
                    "end": 33,
                    "count_group": "per side",
                    "subpart": "leaf lobe",
                },
            ],
        )

    def test_count_44(self):
        self.assertEqual(
            test("sepals absent;"),
            [
                {"flower_part": "sepal", "trait": "flower_part", "start": 0, "end": 6},
                {
                    "low": 0,
                    "trait": "count",
                    "flower_part": "sepal",
                    "start": 7,
                    "end": 13,
                },
            ],
        )

    def test_count_45(self):
        self.maxDiff = None
        self.assertEqual(
            test(
                """
                staminate catkins in 1 or more clusters of 3--6;
                pistillate catkins in 1 or more clusters of 2--7
                """
            ),
            [
                {"sex": "staminate", "trait": "sex", "start": 0, "end": 9},
                {
                    "inflorescence": "catkin",
                    "trait": "inflorescence",
                    "start": 10,
                    "end": 17,
                    "sex": "staminate",
                },
                {
                    "low": 3,
                    "high": 6,
                    "trait": "count",
                    "start": 21,
                    "end": 47,
                    "count_group": "cluster",
                    "inflorescence": "catkin",
                    "sex": "staminate",
                },
                {"sex": "pistillate", "trait": "sex", "start": 49, "end": 59},
                {
                    "inflorescence": "catkin",
                    "trait": "inflorescence",
                    "start": 60,
                    "end": 67,
                    "sex": "pistillate",
                },
                {
                    "low": 2,
                    "high": 7,
                    "trait": "count",
                    "start": 71,
                    "end": 97,
                    "count_group": "cluster",
                    "inflorescence": "catkin",
                    "sex": "pistillate",
                },
            ],
        )

    def test_count_46(self):
        self.assertEqual(
            test("Seeds 1000"),
            [{"end": 5, "fruit_part": "seed", "start": 0, "trait": "fruit_part"}],
        )

    def test_count_47(self):
        self.assertEqual(
            test("leaves with 10 or more pinna pairs"),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "low": 10,
                    "trait": "count",
                    "start": 12,
                    "end": 34,
                    "count_group": "pairs",
                    "per_part": "pinna",
                    "leaf_part": "leaf",
                },
            ],
        )

    def test_count_48(self):
        self.assertEqual(
            test("(see Chapter 2 — Wood and Bark Anatomy)"),
            [{"plant_part": "bark", "trait": "plant_part", "start": 26, "end": 30}],
        )

    def test_count_49(self):
        self.assertEqual(
            test("in 1885, nos, 323 in flower"),
            [{"end": 27, "flower_part": "flower", "start": 21, "trait": "flower_part"}],
        )

    def test_count_50(self):
        self.assertEqual(
            test("plant, !-17 Neto "),
            [{"end": 5, "plant_part": "plant", "start": 0, "trait": "plant_part"}],
        )

    def test_count_51(self):
        self.assertEqual(
            test("plant RO-173"),
            [{"end": 5, "plant_part": "plant", "start": 0, "trait": "plant_part"}],
        )

    def test_count_52(self):
        self.assertEqual(
            test("""7.5’ shrubs."""),
            [{"end": 11, "plant_part": "shrub", "start": 5, "trait": "plant_part"}],
        )
