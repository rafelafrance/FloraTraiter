import unittest

from tests.setup import test2


class TestDeterminer(unittest.TestCase):
    def test_determiner_01(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            test2("""Det;; N. H Russell 195"""),
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
