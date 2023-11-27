import unittest

from flora.pylib.rules.id_number import IdNumber
from flora.pylib.rules.job import Job
from tests.setup import parse


class TestDeterminer(unittest.TestCase):
    def test_determiner_01(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            parse("""Det;; N. H Russell 195"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=18,
                    job="determiner",
                    name="N. H Russell",
                    has_label=True,
                ),
                IdNumber(
                    trait="id_number",
                    start=19,
                    end=22,
                    number="195",
                    type="record_number",
                ),
            ],
        )

    def test_determiner_02(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            parse("""Det. Carter Rosston & Allan Nelson"""),
            [
                Job(
                    trait="job",
                    name=["Carter Rosston", "Allan Nelson"],
                    job="determiner",
                    start=0,
                    end=34,
                    has_label=True,
                )
            ],
        )

    def test_determiner_03(self):
        """It gets lower case name parts."""
        self.assertEqual(
            parse("""det. H. van der Werff & G. McPherson"""),
            [
                Job(
                    trait="job",
                    name=["H. van der Werff", "G. McPherson"],
                    job="determiner",
                    start=0,
                    end=36,
                    has_label=True,
                )
            ],
        )

    def test_determiner_04(self):
        self.assertEqual(
            parse(
                """
                Reveal
                det. James L. Reveal 1971 =
                """
            ),
            [
                Job(
                    trait="job",
                    start=7,
                    end=27,
                    job="determiner",
                    name="James L. Reveal",
                    has_label=True,
                )
            ],
        )
