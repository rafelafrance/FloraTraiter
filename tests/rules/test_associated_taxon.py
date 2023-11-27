import unittest

from flora.pylib.rules.associated_taxon_label import AssociatedTaxonLabel
from flora.pylib.rules.taxon import Taxon
from tests.setup import parse


class TestAssociatedTaxon(unittest.TestCase):
    def test_associated_taxon_01(self):
        """It labels a primary and associated taxa."""
        self.assertEqual(
            parse(
                """
                Cephalanthus occidentalis L. Rubiaceas
                Associated species: Cornus obliqua
                """
            ),
            [
                Taxon(
                    taxon="Cephalanthus occidentalis",
                    rank="species",
                    trait="taxon",
                    start=0,
                    end=38,
                    authority="L. Rubiaceas",
                ),
                AssociatedTaxonLabel(
                    label="associated species",
                    trait="assoc_taxon_label",
                    start=39,
                    end=57,
                ),
                Taxon(
                    rank="species",
                    trait="taxon",
                    start=59,
                    end=73,
                    taxon="Cornus obliqua",
                    associated=True,
                ),
            ],
        )

    def test_associated_taxon_02(self):
        """It does not label the first taxon after the label."""
        self.assertEqual(
            parse("""Associated species: Cornus obliqua"""),
            [
                AssociatedTaxonLabel(
                    label="associated species",
                    trait="assoc_taxon_label",
                    start=0,
                    end=18,
                ),
                Taxon(
                    rank="species",
                    trait="taxon",
                    start=20,
                    end=34,
                    taxon="Cornus obliqua",
                    associated=True,
                ),
            ],
        )

    def test_associated_taxon_03(self):
        """It does not label a higher taxon as primary."""
        self.assertEqual(
            parse(
                """
                Fabaceae
                Cephalanthus occidentalis L. Rubiaceas
                Associated species: Cornus obliqua
                """
            ),
            [
                Taxon(
                    rank="family",
                    trait="taxon",
                    start=0,
                    end=8,
                    taxon="Fabaceae",
                    associated=True,
                ),
                Taxon(
                    taxon="Cephalanthus occidentalis",
                    rank="species",
                    trait="taxon",
                    start=9,
                    end=47,
                    authority="L. Rubiaceas",
                ),
                AssociatedTaxonLabel(
                    label="associated species",
                    trait="assoc_taxon_label",
                    start=48,
                    end=66,
                ),
                Taxon(
                    rank="species",
                    trait="taxon",
                    start=68,
                    end=82,
                    taxon="Cornus obliqua",
                    associated=True,
                ),
            ],
        )

    def test_associated_taxon_04(self):
        """It does not label the first taxon after the label."""
        self.assertEqual(
            parse(""" Cornus obliqua near Cephalanthus occidentalis """),
            [
                Taxon(
                    taxon="Cornus obliqua",
                    rank="species",
                    trait="taxon",
                    start=0,
                    end=14,
                ),
                Taxon(
                    taxon="Cephalanthus occidentalis",
                    rank="species",
                    trait="taxon",
                    start=20,
                    end=45,
                    associated=True,
                ),
            ],
        )
