import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "taxon_like"


class TestTaxonLike(unittest.TestCase):
    def test_taxon_like_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "it is similar to M. sensitiva.")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {
                    "taxonLikeReference": "Mimosa sensitiva",
                    "taxonLikeRelationship": "similar",
                },
            },
        )
