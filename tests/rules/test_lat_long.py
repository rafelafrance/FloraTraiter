import unittest

from tests.setup import parse
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.habitat import Habitat
from traiter.pylib.rules.lat_long import LatLong


class TestLatLong(unittest.TestCase):
    def test_lat_long_01(self):
        self.assertEqual(
            parse("""Grassland, GPS 30° 49’ 27’ N, 99" 15' 22 W May"""),
            [
                Habitat(habitat="grassland", trait="habitat", start=0, end=9),
                LatLong(
                    lat_long="""30° 49’ 27’ N, 99" 15' 22 W""",
                    trait="lat_long",
                    start=11,
                    end=42,
                ),
            ],
        )

    def test_lat_long_02(self):
        self.assertEqual(
            parse("""floodplain wetland. 40.104905N, 79.324561W NAD83"""),
            [
                Habitat(
                    end=18,
                    habitat="floodplain wetland",
                    start=0,
                    trait="habitat",
                ),
                LatLong(
                    lat_long="""40.104905 N, 79.324561 W""",
                    trait="lat_long",
                    datum="NAD83",
                    start=20,
                    end=48,
                ),
            ],
        )

    def test_lat_long_03(self):
        self.assertEqual(
            parse("""32° 19.517' N 110° 40.242' W Elev: 1217m"""),
            [
                LatLong(
                    lat_long="""32° 19.517' N 110° 40.242' W""",
                    trait="lat_long",
                    start=0,
                    end=28,
                ),
                Elevation(
                    elevation=1217.0,
                    trait="elevation",
                    start=29,
                    end=40,
                    units="m",
                ),
            ],
        )

    def test_lat_long_04(self):
        self.assertEqual(
            parse("""(Ord Mountains 7.5’ Q.: 34°41'32"N, 116°49'25"W, +1000m)"""),
            [
                LatLong(
                    lat_long="""34° 41' 32" N, 116° 49' 25" W""",
                    uncertainty=1000.0,
                    trait="lat_long",
                    start=24,
                    end=56,
                    units="m",
                )
            ],
        )

    def test_lat_long_05(self):
        self.assertEqual(
            parse("""43.963272° N, 113.446226° W Uncertainty: 100 m."""),
            [
                LatLong(
                    lat_long="""43.963272° N, 113.446226° W""",
                    uncertainty=100.0,
                    trait="lat_long",
                    start=0,
                    end=47,
                    units="m",
                )
            ],
        )

    def test_lat_long_06(self):
        self.assertEqual(
            parse("""N 33 deg 27' 33", W 111 deg 56' 35","""),
            [
                LatLong(
                    lat_long="""N 33 deg 27' 33", W 111 deg 56' 35\"""",
                    trait="lat_long",
                    start=0,
                    end=35,
                )
            ],
        )

    def test_lat_long_07(self):
        self.assertEqual(
            parse("""40.104905N, 79.324561W NAD83."""),
            [
                LatLong(
                    datum="NAD83",
                    lat_long="40.104905 N, 79.324561 W",
                    trait="lat_long",
                    start=0,
                    end=28,
                )
            ],
        )

    def test_lat_long_08(self):
        self.assertEqual(
            parse("""33° 53' 31.0" N, -111° 56' 59.9" W"""),
            [
                LatLong(
                    lat_long="""33° 53' 31.0" N, -111° 56' 59.9" W""",
                    trait="lat_long",
                    start=0,
                    end=34,
                )
            ],
        )

    def test_lat_long_09(self):
        self.assertEqual(
            parse("""Lat: 41.01102 Long: -75.485306 (WGS-84)"""),
            [
                LatLong(
                    datum="WGS84",
                    lat_long="""Lat: 41.01102 Long: -75.485306""",
                    trait="lat_long",
                    start=0,
                    end=39,
                )
            ],
        )

    def test_lat_long_10(self):
        self.assertEqual(
            parse("""Lat.: 36° 21'"N Long.: 112° 40'"W"""),
            [
                LatLong(
                    lat_long="""Lat.: 36° 21'" N Long.: 112° 40'" W""",
                    trait="lat_long",
                    start=0,
                    end=33,
                )
            ],
        )

    def test_lat_long_11(self):
        self.assertEqual(
            parse("""N 33° 27’ W 111° 56 35" 1200 ft.,"""),
            [
                LatLong(
                    lat_long='''N 33° 27’ W 111° 56 35"''',
                    uncertainty=365.76,
                    trait="lat_long",
                    start=0,
                    end=33,
                    units="m",
                )
            ],
        )

    def test_lat_long_12(self):
        """It handles a lat/long range."""
        self.assertEqual(
            parse("""Lat. 13.5° - 14°55'S Long. 60.2° - 61°50'W."""),
            [
                LatLong(
                    lat_long="""Lat. 13.5° -14° 55'S Long. 60.2° -61° 50' W.""",
                    trait="lat_long",
                    start=0,
                    end=43,
                )
            ],
        )

    def test_lat_long_13(self):
        self.assertEqual(
            parse("""45.01701° N, 118.15694° W Uncertainty: 50 m.; Datum: WGS 84;"""),
            [
                LatLong(
                    lat_long="45.01701° N, 118.15694° W",
                    uncertainty=50.0,
                    datum="WGS84",
                    trait="lat_long",
                    start=0,
                    end=59,
                    units="m",
                )
            ],
        )

    def test_lat_long_14(self):
        self.assertEqual(
            parse("""N41° 50.046’ W087° 54.172’."""),
            [
                LatLong(
                    lat_long="N41° 50.046’ W087° 54.172’",
                    trait="lat_long",
                    start=0,
                    end=26,
                )
            ],
        )

    def test_lat_long_15(self):
        self.assertEqual(
            parse("""27.409578°, -80.397773°"""),
            [
                LatLong(
                    lat_long="27.409578°, -80.397773°",
                    trait="lat_long",
                    start=0,
                    end=23,
                )
            ],
        )

    def test_lat_long_16(self):
        self.assertEqual(
            parse("""Q.: 34°37'17"N, 116°50'15"W,+1000m)"""),
            [
                LatLong(
                    lat_long="""34° 37' 17" N, 116° 50' 15" W""",
                    trait="lat_long",
                    uncertainty=1000.0,
                    start=4,
                    end=35,
                    units="m",
                )
            ],
        )

    def test_lat_long_17(self):
        self.assertEqual(
            parse("""Lat. 29°12.063'N Long. 082°02.005'W Datum: WGS 84."""),
            [
                LatLong(
                    lat_long="Lat. 29° 12.063' N Long. 082° 02.005' W",
                    trait="lat_long",
                    datum="WGS84",
                    start=0,
                    end=49,
                )
            ],
        )

    def test_lat_long_18(self):
        self.assertEqual(
            parse("""34° 29' 09.4" N 111° 46' 18.9" W +-50 meters"""),
            [
                LatLong(
                    lat_long="""34° 29' 09.4" N 111° 46' 18.9" W""",
                    trait="lat_long",
                    start=0,
                    end=44,
                    units="m",
                    uncertainty=50.0,
                )
            ],
        )

    def test_lat_long_19(self):
        self.assertEqual(
            parse(
                """40.104905N,
                79.324561W NAD83."""
            ),
            [
                LatLong(
                    lat_long="""40.104905 N, 79.324561 W""",
                    datum="NAD83",
                    trait="lat_long",
                    start=0,
                    end=28,
                )
            ],
        )

    def test_lat_long_20(self):
        self.assertEqual(
            parse("""35°50-52'S 71°10-20'W 750-900 m"""),
            [
                LatLong(
                    lat_long="""35° 50 -52'S 71° 10 -20' W""",
                    uncertainty=900.0,
                    units="m",
                    trait="lat_long",
                    start=0,
                    end=31,
                )
            ],
        )

    def test_lat_long_21(self):
        self.assertEqual(
            parse("""33.65517 -111.84455 619 Meters"""),
            [
                LatLong(
                    lat_long="""33.65517 -111.84455""",
                    uncertainty=619.0,
                    units="m",
                    trait="lat_long",
                    start=0,
                    end=30,
                )
            ],
        )
