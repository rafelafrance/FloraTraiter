import unittest

from tests.setup import full_test


class TestLocality(unittest.TestCase):
    def test_locality_01(self):
        self.assertEqual(
            full_test("""5 miles North of Mason off Hwy 386."""),
            [
                {
                    "locality": "5 miles North of Mason off Hwy 386.",
                    "trait": "locality",
                    "start": 0,
                    "end": 35,
                }
            ],
        )

    def test_locality_02(self):
        self.assertEqual(
            full_test(
                """
                Tunkhannock Twp. Pocono Pines Quadrangle. Mud Run, Stonecrest Park,.16
                miles SSW of Long Pond, PA. Headwaters wetland of Indiana Mountains
                Lake.
                """
            ),
            [
                {
                    "locality": "Tunkhannock Twp.",
                    "trait": "locality",
                    "start": 0,
                    "end": 16,
                },
                {
                    "locality": "Pocono Pines Quadrangle.",
                    "trait": "locality",
                    "start": 17,
                    "end": 41,
                },
                {
                    "locality": "Mud Run, Stonecrest Park,"
                    ".16 miles SSW of Long Pond, PA.",
                    "trait": "locality",
                    "start": 42,
                    "end": 98,
                },
                {
                    "locality": "Headwaters wetland of Indiana Mountains Lake.",
                    "trait": "locality",
                    "start": 99,
                    "end": 144,
                },
            ],
        )

    def test_locality_03(self):
        self.assertEqual(
            full_test("""; files. purple."""),
            [],
        )

    def test_locality_04(self):
        self.assertEqual(
            full_test("""(Florida's Turnpike)"""),
            [
                {
                    "locality": "Florida's Turnpike",
                    "trait": "locality",
                    "start": 0,
                    "end": 19,
                }
            ],
        )

    def test_locality_05(self):
        self.assertEqual(
            full_test(
                """
                Wallowa-Whitman National Forest, Forest Service Road 7312.
                """
            ),
            [
                {
                    "locality": "Wallowa-Whitman National Forest, Forest Service "
                    "Road 7312.",
                    "trait": "locality",
                    "start": 0,
                    "end": 58,
                },
            ],
        )

    def test_locality_06(self):
        self.assertEqual(
            full_test(
                """Sonoran Desert scrub, disturbed trail side. Occasional annual."""
            ),
            [
                {
                    "habitat": "sonoran desert scrub",
                    "trait": "habitat",
                    "start": 0,
                    "end": 20,
                },
                {
                    "locality": "disturbed trail side.",
                    "trait": "locality",
                    "start": 22,
                    "end": 43,
                },
                {
                    "plant_duration": "annual",
                    "trait": "plant_duration",
                    "start": 55,
                    "end": 61,
                },
            ],
        )

    def test_locality_07(self):
        self.assertEqual(
            full_test(
                """
                Arizona Uppland Sonoran Desert desert scrub, flats.
                Sandy soil Local erecta annual,
                """
            ),
            [
                {
                    "habitat": "uppland sonoran desert desert scrub flats",
                    "trait": "habitat",
                    "start": 8,
                    "end": 50,
                },
                {"habitat": "sandy soil", "trait": "habitat", "start": 52, "end": 62},
                {
                    "plant_duration": "annual",
                    "trait": "plant_duration",
                    "start": 76,
                    "end": 82,
                },
            ],
        )

    def test_locality_08(self):
        self.assertEqual(
            full_test("""Scattered on edge of forest;"""),
            [{"end": 27, "habitat": "edge of forest", "start": 13, "trait": "habitat"}],
        )

    def test_locality_09(self):
        self.assertEqual(
            full_test("""lobes turned out or black."""),
            [
                {"trait": "subpart", "subpart": "lobe", "start": 0, "end": 5},
                {
                    "color": "black",
                    "trait": "color",
                    "start": 20,
                    "end": 25,
                    "subpart": "lobe",
                },
            ],
        )

    def test_locality_10(self):
        self.assertEqual(
            full_test(
                """
                LOCATION Along Rte. 39, 9.1 mi SEof Santiago Papasquiaro.
                HABITAT Pine-juniper-oak-acacia zone.
                """
            ),
            [
                {
                    "locality": "Along Rte. 39, 9.1 mi SEof Santiago Papasquiaro.",
                    "labeled": True,
                    "trait": "locality",
                    "start": 0,
                    "end": 57,
                },
                {
                    "habitat": "Pine-juniper-oak-acacia zone.",
                    "trait": "habitat",
                    "start": 58,
                    "end": 95,
                },
            ],
        )

    def test_locality_11(self):
        self.assertEqual(
            full_test(
                """
                Fruit is a
                grape and is dark purple in color.
                """
            ),
            [
                {"fruit_part": "fruit", "trait": "fruit_part", "start": 0, "end": 5},
                {
                    "color": "purple-in-color",
                    "trait": "color",
                    "start": 24,
                    "end": 44,
                    "fruit_part": "fruit",
                },
            ],
        )

    def test_locality_12(self):
        self.assertEqual(
            full_test("""Monteverde. Elev. 1400- 1500 m. Lower montane rainforest"""),
            [
                {
                    "trait": "elevation",
                    "elevation": 1400.0,
                    "elevation_high": 1500.0,
                    "units": "m",
                    "start": 12,
                    "end": 31,
                },
                {
                    "end": 56,
                    "habitat": "montane rain forest",
                    "start": 38,
                    "trait": "habitat",
                },
            ],
        )
