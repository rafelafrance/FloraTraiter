import unittest

from tests.setup import test2


class TestAssociatedTaxon(unittest.TestCase):
    def test_associated_taxon_01(self):
        """It labels a primary and associated taxa."""
        self.assertEqual(
            test2(
                """
                Cephalanthus occidentalis L. Rubiaceas
                Associated species: Cornus obliqua
                """
            ),
            [
                {
                    "taxon": "Cephalanthus occidentalis",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 38,
                    "authority": "L. Rubiaceas",
                },
                {
                    "assoc_taxon_label": "associated species",
                    "trait": "assoc_taxon_label",
                    "start": 39,
                    "end": 57,
                },
                {
                    "rank": "species",
                    "trait": "associated_taxon",
                    "start": 59,
                    "end": 73,
                    "associated_taxon": "Cornus obliqua",
                },
            ],
        )

    def test_associated_taxon_02(self):
        """It does not label the first taxon after the label."""
        self.assertEqual(
            test2("""Associated species: Cornus obliqua"""),
            [
                {
                    "assoc_taxon_label": "associated species",
                    "trait": "assoc_taxon_label",
                    "start": 0,
                    "end": 18,
                },
                {
                    "rank": "species",
                    "trait": "associated_taxon",
                    "start": 20,
                    "end": 34,
                    "associated_taxon": "Cornus obliqua",
                },
            ],
        )

    def test_associated_taxon_03(self):
        """It does not label a higher taxon as primary."""
        self.assertEqual(
            test2(
                """
                Fabaceae
                Cephalanthus occidentalis L. Rubiaceas
                Associated species: Cornus obliqua
                """
            ),
            [
                {
                    "rank": "family",
                    "trait": "associated_taxon",
                    "start": 0,
                    "end": 8,
                    "associated_taxon": "Fabaceae",
                },
                {
                    "taxon": "Cephalanthus occidentalis",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 9,
                    "end": 47,
                    "authority": "L. Rubiaceas",
                },
                {
                    "assoc_taxon_label": "associated species",
                    "trait": "assoc_taxon_label",
                    "start": 48,
                    "end": 66,
                },
                {
                    "rank": "species",
                    "trait": "associated_taxon",
                    "start": 68,
                    "end": 82,
                    "associated_taxon": "Cornus obliqua",
                },
            ],
        )

    def test_associated_taxon_04(self):
        """It does not label the first taxon after the label."""
        self.assertEqual(
            test2(""" Cornus obliqua near Cephalanthus occidentalis """),
            [
                {
                    "taxon": "Cornus obliqua",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 14,
                },
                {
                    "associated_taxon": "Cephalanthus occidentalis",
                    "rank": "species",
                    "trait": "associated_taxon",
                    "start": 20,
                    "end": 45,
                },
            ],
        )
