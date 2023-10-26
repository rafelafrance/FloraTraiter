import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "taxon"


class TestTaxon(unittest.TestCase):
    def test_taxon_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "M. sensitiva")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "scientificName": "Mimosa sensitiva",
                "taxonRank": "species",
                "dynamicProperties": {"primaryTaxon": 1},
            },
        )

    def test_taxon_02(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "A. pachyphloia subsp. brevipinnula")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "scientificName": "Acacia pachyphloia subsp. brevipinnula",
                "taxonRank": "subspecies",
                "dynamicProperties": {"primaryTaxon": 1},
            },
        )

    def test_taxon_03(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "A. pachyphloia Britton & Rose")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "scientificName": "Acacia pachyphloia",
                "taxonRank": "species",
                "scientificNameAuthorship": "Britton and Rose",
                "dynamicProperties": {"primaryTaxon": 1},
            },
        )
