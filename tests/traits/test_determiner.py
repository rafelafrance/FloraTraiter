import unittest

from flora.pylib.traits.job import Job
from tests.setup import full_test


class TestDeterminer(unittest.TestCase):
    def test_determiner_01(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            full_test("""Det;; N. H Russell 195"""),
            [
                Job(
                    trait="job",
                    id_no="195",
                    name="N. H Russell",
                    job="determiner",
                    start=0,
                    end=22,
                )
            ],
        )

    def test_determiner_02(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            full_test("""Det. Carter Rosston & Allan Nelson"""),
            [
                Job(
                    trait="job",
                    name=["Carter Rosston", "Allan Nelson"],
                    job="determiner",
                    start=0,
                    end=34,
                )
            ],
        )

    def test_determiner_03(self):
        """It gets lower case name parts."""
        self.assertEqual(
            full_test("""det. H. van der Werff & G. McPherson"""),
            [
                Job(
                    trait="job",
                    name=["H. van der Werff", "G. McPherson"],
                    job="determiner",
                    start=0,
                    end=36,
                )
            ],
        )

    def test_determiner_04(self):
        self.assertEqual(
            full_test(
                """
                Reveal
                det. James L. Reveal 1971 =
                """
            ),
            [
                Job(
                    trait="job",
                    name="James L. Reveal",
                    id_no="1971",
                    job="determiner",
                    start=7,
                    end=32,
                )
            ],
        )
