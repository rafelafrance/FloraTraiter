import unittest

from tests.setup import test


class TestTaxonLikeLinker(unittest.TestCase):
    def test_taxon_like_linker_01(self):
        self.assertEqual(
            test("""Mimosa sensitiva Bameby, vicinis A. pachyphloia"""),
            [
                {
                    "rank": "species",
                    "authority": "Bameby",
                    "taxon": "Mimosa sensitiva",
                    "trait": "taxon",
                    "start": 0,
                    "end": 23,
                    "taxon_like": "Acacia pachyphloia",
                },
                {
                    "rank": "species",
                    "trait": "taxon_like",
                    "start": 25,
                    "end": 47,
                    "taxon_like": "Acacia pachyphloia",
                    "relation": "vicinis",
                },
            ],
        )
