import unittest

from tests.setup import to_ent

LABEL = "taxon_like"


class TestTaxonLike(unittest.TestCase):
    def test_taxon_like_01(self):
        ent = to_ent(LABEL, "it is similar to M. sensitiva.")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:dynamicProperties": {
                    "taxonLikeReference": "Mimosa sensitiva",
                    "taxonLikeRelationship": "similar",
                },
            },
        )
