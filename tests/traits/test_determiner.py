import unittest

from tests.setup import full_test


class TestDeterminer(unittest.TestCase):
    def test_determiner_01(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            full_test("""Det;; N. H Russell 195"""),
            [
                {
                    "determiner_no": "195",
                    "determiner": "N. H Russell",
                    "trait": "determiner",
                    "start": 0,
                    "end": 22,
                }
            ],
        )

    def test_determiner_02(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            full_test("""Det. Carter Rosston & Allan Nelson"""),
            [
                {
                    "determiner": "Carter Rosston & Allan Nelson",
                    "trait": "determiner",
                    "start": 0,
                    "end": 34,
                }
            ],
        )

    def test_determiner_03(self):
        """It gets lower case name parts."""
        self.assertEqual(
            full_test("""det. H. van der Werff & G. McPherson"""),
            [
                {
                    "determiner": "H. van der Werff & G. McPherson",
                    "trait": "determiner",
                    "start": 0,
                    "end": 36,
                }
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
                {
                    "determiner": "James L. Reveal",
                    "determiner_no": "1971",
                    "trait": "determiner",
                    "start": 7,
                    "end": 32,
                }
            ],
        )
