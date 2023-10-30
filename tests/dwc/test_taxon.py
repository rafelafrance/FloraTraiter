import unittest

from tests.setup import to_ent

LABEL = "taxon"


class TestTaxon(unittest.TestCase):
    def test_taxon_01(self):
        ent = to_ent(LABEL, "M. sensitiva")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "scientificName": "Mimosa sensitiva",
                "taxonRank": "species",
                "dynamicProperties": {"primaryTaxon": 1},
            },
        )

    def test_taxon_02(self):
        ent = to_ent(LABEL, "A. pachyphloia subsp. brevipinnula")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "scientificName": "Acacia pachyphloia subsp. brevipinnula",
                "taxonRank": "subspecies",
                "dynamicProperties": {"primaryTaxon": 1},
            },
        )

    def test_taxon_03(self):
        ent = to_ent(LABEL, "A. pachyphloia Britton & Rose")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "scientificName": "Acacia pachyphloia",
                "taxonRank": "species",
                "scientificNameAuthorship": "Britton and Rose",
                "dynamicProperties": {"primaryTaxon": 1},
            },
        )
