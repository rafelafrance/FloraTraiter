import unittest

from tests.setup import to_dwc

LABEL = "taxon_like"


class TestTaxonLike(unittest.TestCase):
    def test_taxon_like_01(self):
        self.assertEqual(
            to_dwc(LABEL, "it is similar to M. sensitiva."),
            {"dwc:associatedTaxa": "similar: Mimosa sensitiva"},
        )
