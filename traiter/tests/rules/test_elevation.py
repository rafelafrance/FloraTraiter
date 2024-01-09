import unittest

from tests.setup import parse
from traiter.traiter.pylib.rules.elevation import Elevation


class TestElevation(unittest.TestCase):
    def test_elevation_01(self):
        """It handles metric units."""
        self.assertEqual(
            parse(""" Elevation: 1463m """),
            [
                Elevation(
                    trait="elevation",
                    elevation=1463.0,
                    units="m",
                    start=0,
                    end=16,
                ),
            ],
        )

    def test_elevation_02(self):
        """It handles a measurement in different units."""
        self.assertEqual(
            parse(""" Elev: 782m. (2566 ft) """),
            [
                Elevation(
                    trait="elevation",
                    elevation=782.0,
                    units="m",
                    start=0,
                    end=21,
                ),
            ],
        )

    def test_elevation_03(self):
        """It handles a range."""
        traits = parse(""" Elev. 9,500-9640 ft. """)
        self.assertEqual(traits[0].trait, "elevation")
        self.assertEqual(traits[0].start, 0)
        self.assertEqual(traits[0].end, 19)
        self.assertEqual(traits[0].units, "m")
        self.assertAlmostEqual(traits[0].elevation, 2895.6)
        self.assertAlmostEqual(traits[0].elevation_high, 2938.272)

    def test_elevation_04(self):
        """Make sure punctuation is not interpreted as numbers."""
        self.assertEqual(
            parse(""" alt., 250 m. """),
            [
                Elevation(
                    trait="elevation",
                    elevation=250.0,
                    units="m",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_elevation_05(self):
        self.assertEqual(
            parse("""Alto.: 834m/2735ft."""),
            [
                Elevation(
                    trait="elevation",
                    elevation=834.0,
                    units="m",
                    start=0,
                    end=18,
                ),
            ],
        )

    def test_elevation_06(self):
        self.assertEqual(
            parse("""Elev. ca, 200 m."""),
            [
                Elevation(
                    trait="elevation",
                    elevation=200.0,
                    units="m",
                    about=True,
                    start=0,
                    end=16,
                ),
            ],
        )

    def test_elevation_07(self):
        self.assertEqual(
            parse("""975m/3200ft"""),
            [
                Elevation(
                    trait="elevation",
                    elevation=975.0,
                    units="m",
                    start=0,
                    end=11,
                ),
            ],
        )

    def test_elevation_08(self):
        traits = parse("""Elev. ca. 460 - 470 ft""")
        self.assertEqual(traits[0].trait, "elevation")
        self.assertEqual(traits[0].start, 0)
        self.assertEqual(traits[0].end, 22)
        self.assertEqual(traits[0].units, "m")
        self.assertAlmostEqual(traits[0].elevation, 140.208)
        self.assertAlmostEqual(traits[0].elevation_high, 143.256)

    def test_elevation_09(self):
        self.assertEqual(
            parse("""elev: 737m. (2417 ft.)"""),
            [
                Elevation(
                    trait="elevation",
                    elevation=737.0,
                    units="m",
                    start=0,
                    end=22,
                ),
            ],
        )

    def test_elevation_10(self):
        self.assertEqual(
            parse(
                """Elev.
                1400- 1500 m.
                """,
            ),
            [
                Elevation(
                    trait="elevation",
                    elevation=1400.0,
                    elevation_high=1500.0,
                    units="m",
                    start=0,
                    end=19,
                ),
            ],
        )

    def test_elevation_11(self):
        self.assertEqual(
            parse("""Elev 85’."""),
            [
                Elevation(
                    trait="elevation",
                    elevation=25.908,
                    units="m",
                    start=0,
                    end=8,
                ),
            ],
        )
