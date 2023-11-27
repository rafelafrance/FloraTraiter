import unittest

from flora.pylib.rules.taxon import Taxon
from flora.pylib.rules.taxon_like import TaxonLike
from tests.setup import parse


class TestTaxonLikeLinker(unittest.TestCase):
    def test_taxon_like_linker_01(self):
        self.maxDiff = None
        self.assertEqual(
            parse("""Mimosa sensitiva Bameby, vicinis A. pachyphloia"""),
            [
                Taxon(
                    rank="species",
                    authority="Bameby",
                    taxon="Mimosa sensitiva",
                    trait="taxon",
                    start=0,
                    end=24,
                    taxon_like="Acacia pachyphloia",
                ),
                TaxonLike(
                    trait="taxon_like",
                    start=25,
                    end=47,
                    taxon_like="Acacia pachyphloia",
                    relation="vicinis",
                ),
            ],
        )
