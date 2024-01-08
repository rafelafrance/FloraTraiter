import unittest

from tests.setup import parse
from traiter.traiter.pylib.rules.color import Color


class TestColor(unittest.TestCase):
    def test_color_01(self):
        self.assertEqual(
            parse(
                """hypanthium green or greenish yellow,
                usually not purple-spotted, rarely purple-spotted distally.
                """,
            ),
            [
                Color(
                    color="green",
                    trait="color",
                    start=11,
                    end=16,
                ),
                Color(
                    color="green-yellow",
                    trait="color",
                    start=20,
                    end=35,
                ),
                Color(
                    color="purple-spotted",
                    missing=True,
                    trait="color",
                    start=45,
                    end=63,
                ),
                Color(
                    color="purple-spotted",
                    missing=True,
                    trait="color",
                    start=65,
                    end=86,
                ),
            ],
        )

    def test_color_02(self):
        self.assertEqual(
            parse("hypanthium straw-colored to sulphur-yellow or golden-yellow."),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=11,
                    end=24,
                ),
                Color(
                    color="yellow",
                    trait="color",
                    start=28,
                    end=42,
                ),
                Color(
                    color="yellow",
                    trait="color",
                    start=46,
                    end=59,
                ),
            ],
        )

    def test_color_03(self):
        self.assertEqual(
            parse("sepals erect, green- or red-tipped."),
            [
                Color(
                    color="green",
                    trait="color",
                    start=14,
                    end=20,
                ),
                Color(
                    color="red-tipped",
                    trait="color",
                    start=24,
                    end=34,
                ),
            ],
        )

    def test_color_04(self):
        self.assertEqual(
            parse("petals white, cream, or pale green [orange to yellow]."),
            [
                Color(
                    color="white",
                    trait="color",
                    start=7,
                    end=12,
                ),
                Color(
                    color="white",
                    trait="color",
                    start=14,
                    end=19,
                ),
                Color(
                    color="green",
                    trait="color",
                    start=24,
                    end=34,
                ),
                Color(
                    color="orange",
                    trait="color",
                    start=36,
                    end=42,
                ),
                Color(
                    color="yellow",
                    trait="color",
                    start=46,
                    end=52,
                ),
            ],
        )

    def test_color_05(self):
        """It handles pattern notations within colors."""
        self.maxDiff = None
        self.assertEqual(
            parse(
                """
                petals distinct, white to cream, greenish yellow,
                maturing yellowish or pale brown, commonly mottled or with
                light green or white longitudinal stripes.
                """,
            ),
            [
                Color(
                    color="white",
                    trait="color",
                    start=17,
                    end=22,
                ),
                Color(
                    color="white",
                    trait="color",
                    start=26,
                    end=31,
                ),
                Color(
                    color="green-yellow",
                    trait="color",
                    start=33,
                    end=48,
                ),
                Color(
                    color="yellow",
                    trait="color",
                    start=59,
                    end=68,
                ),
                Color(
                    color="brown",
                    trait="color",
                    start=72,
                    end=82,
                ),
                Color(
                    color="green",
                    trait="color",
                    start=109,
                    end=120,
                ),
                Color(
                    color="white-longitudinal-stripes",
                    trait="color",
                    start=124,
                    end=150,
                ),
            ],
        )

    def test_color_06(self):
        self.assertEqual(
            parse(
                """
                Petals distinct, white to cream, greenish white,
                or yellowish green, or yellowish, usually green-throated
                and faintly green-lined.
                """,
            ),
            [
                Color(
                    color="white",
                    trait="color",
                    start=17,
                    end=22,
                ),
                Color(
                    color="white",
                    trait="color",
                    start=26,
                    end=31,
                ),
                Color(
                    color="green-white",
                    trait="color",
                    start=33,
                    end=47,
                ),
                Color(
                    color="yellow-green",
                    trait="color",
                    start=52,
                    end=67,
                ),
                Color(
                    color="yellow",
                    trait="color",
                    start=72,
                    end=81,
                ),
                Color(
                    color="green-throated",
                    trait="color",
                    start=91,
                    end=105,
                ),
                Color(
                    color="green-lined",
                    trait="color",
                    start=110,
                    end=129,
                ),
            ],
        )

    def test_color_07(self):
        self.assertEqual(
            parse("calyx yellow"),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=6,
                    end=12,
                ),
            ],
        )

    def test_color_08(self):
        self.assertEqual(
            parse("corolla yellow"),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=8,
                    end=14,
                ),
            ],
        )

    def test_color_09(self):
        self.assertEqual(
            parse("flower yellow"),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=7,
                    end=13,
                ),
            ],
        )

    def test_color_10(self):
        self.assertEqual(
            parse("hypanthium yellow"),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=11,
                    end=17,
                ),
            ],
        )

    def test_color_11(self):
        self.assertEqual(
            parse("petal pale sulfur-yellow."),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=6,
                    end=24,
                ),
            ],
        )

    def test_color_12(self):
        self.assertEqual(
            parse("sepal yellow"),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=6,
                    end=12,
                ),
            ],
        )

    def test_color_13(self):
        self.assertEqual(
            parse("Leaves acaulescent or nearly so, with white hairs."),
            [
                Color(
                    color="white",
                    trait="color",
                    start=38,
                    end=43,
                ),
            ],
        )

    def test_color_14(self):
        self.assertEqual(
            parse("leaflets surfaces rather densely spotted with blackish dots"),
            [
                Color(
                    color="black-dots",
                    trait="color",
                    start=46,
                    end=59,
                ),
            ],
        )

    def test_color_15(self):
        self.assertEqual(
            parse("Petals purplish in life, whitish yellowish when dry;"),
            [
                Color(
                    color="purple",
                    trait="color",
                    start=7,
                    end=15,
                ),
                Color(
                    color="white-yellow",
                    trait="color",
                    start=25,
                    end=42,
                ),
            ],
        )

    def test_color_16(self):
        self.assertEqual(
            parse("Petals red or golden yellowish"),
            [
                Color(
                    color="red",
                    trait="color",
                    start=7,
                    end=10,
                ),
                Color(
                    color="yellow",
                    trait="color",
                    start=14,
                    end=30,
                ),
            ],
        )

    def test_color_17(self):
        self.assertEqual(
            parse("twigs: young growth green or reddish-tinged."),
            [
                Color(
                    color="green",
                    trait="color",
                    start=20,
                    end=25,
                ),
                Color(
                    color="red-tinged",
                    trait="color",
                    start=29,
                    end=43,
                ),
            ],
        )

    def test_color_18(self):
        self.assertEqual(
            parse(
                """stipules, the young stems and lf-axes hispid with stout, partly
                confluent or branched, yellowish setae""",
            ),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=87,
                    end=96,
                ),
            ],
        )

    def test_color_19(self):
        """It does not repeat colors."""
        self.assertEqual(
            parse("""petals clear lemon yellow."""),
            [
                Color(
                    color="yellow",
                    trait="color",
                    start=13,
                    end=25,
                ),
            ],
        )
