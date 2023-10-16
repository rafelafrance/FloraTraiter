import unittest

from tests.setup import small_test


class TestTaxonLike(unittest.TestCase):
    def test_taxon_like_01(self):
        self.assertEqual(
            small_test("""it seems closer to the nearly sympatric M. sensitiva."""),
            [
                {
                    "rank": "species",
                    "taxon_like": "Mimosa sensitiva",
                    "trait": "taxon_like",
                    "start": 30,
                    "end": 52,
                    "relation": "sympatric",
                }
            ],
        )

    def test_taxon_like_02(self):
        self.assertEqual(
            small_test("""it is similar to M. sensitiva."""),
            [
                {
                    "rank": "species",
                    "taxon_like": "Mimosa sensitiva",
                    "trait": "taxon_like",
                    "start": 6,
                    "end": 29,
                    "relation": "similar",
                }
            ],
        )

    def test_taxon_like_03(self):
        self.assertEqual(
            small_test("""It resembles M. sensitiva in amplitude"""),
            [
                {
                    "rank": "species",
                    "taxon_like": "Mimosa sensitiva",
                    "trait": "taxon_like",
                    "start": 3,
                    "end": 25,
                    "relation": "resembles",
                }
            ],
        )

    def test_taxon_like_04(self):
        self.assertEqual(
            small_test("""sympatric pair of M. sensitiva Harms ex Glaziou"""),
            [
                {
                    "rank": "species",
                    "authority": "Harms and Glaziou",
                    "taxon_like": "Mimosa sensitiva",
                    "trait": "taxon_like",
                    "start": 0,
                    "end": 47,
                    "relation": "sympatric",
                }
            ],
        )

    def test_taxon_like_05(self):
        self.assertEqual(
            small_test("""vicinis M. sensitiva et A. pachyphloia"""),
            [
                {
                    "rank": "species",
                    "taxon_like": ["Mimosa sensitiva", "Acacia pachyphloia"],
                    "trait": "taxon_like",
                    "start": 0,
                    "end": 38,
                    "relation": "vicinis",
                }
            ],
        )

    def test_taxon_like_06(self):
        self.assertEqual(
            small_test("""distinguished from var. pachyphloia"""),
            [
                {
                    "rank": "variety",
                    "trait": "taxon_like",
                    "start": 0,
                    "end": 35,
                    "taxon_like": "pachyphloia",
                    "relation": "distinguished",
                }
            ],
        )

    def test_taxon_like_07(self):
        self.assertEqual(
            small_test("""The var. floridana resembles var. nuttallii in venation"""),
            [
                {
                    "rank": "variety",
                    "taxon": "floridana",
                    "trait": "taxon",
                    "start": 4,
                    "end": 18,
                    "taxon_like": "nuttallii",
                },
                {
                    "rank": "variety",
                    "trait": "taxon_like",
                    "start": 19,
                    "end": 43,
                    "taxon_like": "nuttallii",
                    "relation": "resembles",
                },
                {"venation": "vein", "trait": "venation", "start": 47, "end": 55},
            ],
        )
