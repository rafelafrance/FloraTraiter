import unittest

from tests.setup import to_ent

LABEL = "taxon"


class TestTaxon(unittest.TestCase):
    def test_taxon_01(self):
        ent = to_ent(LABEL, "M. sensitiva")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:scientificName": "Mimosa sensitiva",
                "dwc:taxonRank": "species",
                "dwc:dynamicProperties": {"primaryTaxon": 1},
            },
        )

    def test_taxon_02(self):
        ent = to_ent(LABEL, "A. pachyphloia subsp. brevipinnula")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:scientificName": "Acacia pachyphloia subsp. brevipinnula",
                "dwc:taxonRank": "subspecies",
                "dwc:dynamicProperties": {"primaryTaxon": 1},
            },
        )

    def test_taxon_03(self):
        ent = to_ent(LABEL, "A. pachyphloia Britton & Rose")
        dwc = ent._.trait.to_dwc()
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:scientificName": "Acacia pachyphloia",
                "dwc:taxonRank": "species",
                "dwc:scientificNameAuthorship": "Britton and Rose",
                "dwc:dynamicProperties": {"primaryTaxon": 1},
            },
        )