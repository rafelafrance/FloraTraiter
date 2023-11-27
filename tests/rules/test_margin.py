import unittest

from flora.pylib.rules.margin import Margin
from flora.pylib.rules.subpart import Subpart
from tests.setup import parse


class TestMargin(unittest.TestCase):
    def test_margin_01(self):
        self.assertEqual(
            parse("margin shallowly undulate-crenate"),
            [
                Subpart(subpart="margin", trait="subpart", start=0, end=6),
                Margin(
                    margin="undulate-crenate",
                    trait="margin",
                    subpart="margin",
                    start=7,
                    end=33,
                ),
            ],
        )

    def test_margin_02(self):
        """It removes unattached margins."""
        self.assertEqual(
            parse("reniform, undulate-margined"),
            [],
        )

    def test_margin_03(self):
        self.assertEqual(
            parse("margins thickened-corrugated"),
            [
                Subpart(subpart="margin", trait="subpart", start=0, end=7),
                Margin(
                    margin="corrugated",
                    trait="margin",
                    subpart="margin",
                    start=8,
                    end=28,
                ),
            ],
        )

    def test_margin_04(self):
        self.assertEqual(
            parse("margins coarsely toothed or remotely sinuate-dentate to serrate,"),
            [
                Subpart(subpart="margin", trait="subpart", start=0, end=7),
                Margin(
                    margin="toothed",
                    trait="margin",
                    subpart="margin",
                    start=8,
                    end=24,
                ),
                Margin(
                    margin="sinuate-dentate",
                    trait="margin",
                    subpart="margin",
                    start=28,
                    end=52,
                ),
                Margin(
                    margin="serrate",
                    trait="margin",
                    subpart="margin",
                    start=56,
                    end=63,
                ),
            ],
        )
