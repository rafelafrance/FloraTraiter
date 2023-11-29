import unittest

from tests.setup import to_dwc

LABEL = "taxon"


class TestTaxon(unittest.TestCase):
    def test_taxon_01(self):
        self.assertEqual(
            to_dwc(LABEL, "M. sensitiva"),
            {
                "dwc:scientificName": "M. sensitiva",
                "dwc:taxonRank": "species",
            },
        )

    def test_taxon_02(self):
        self.assertEqual(
            to_dwc(LABEL, "A. pachyphloia subsp. brevipinnula"),
            {
                "dwc:scientificName": "A. pachyphloia subsp. brevipinnula",
                "dwc:taxonRank": "subspecies",
            },
        )

    def test_taxon_03(self):
        self.assertEqual(
            to_dwc(LABEL, "A. pachyphloia Britton & Rose"),
            {
                "dwc:scientificName": "A. pachyphloia Britton & Rose",
                "dwc:taxonRank": "species",
                "dwc:scientificNameAuthorship": "Britton and Rose",
            },
        )

    def test_taxon_04(self):
        self.assertEqual(
            to_dwc(LABEL, "Acacia pachyphloia (L.) Moench. ssp. brevipinnula"),
            {
                "dwc:scientificName": "Acacia pachyphloia (L.) Moench. ssp. brevipinnula",
                "dwc:taxonRank": "subspecies",
                "dwc:scientificNameAuthorship": "Linnaeus, Moench",
            },
        )

    def test_taxon_05(self):
        self.assertEqual(
            to_dwc(LABEL, "Associated species: Cornus obliqua"),
            {
                "dwc:associatedTaxa": "associated: Cornus obliqua",
            },
        )

    def test_taxon_06(self):
        self.assertEqual(
            to_dwc(LABEL, "Cornaceae"),
            {"dwc:family": "Cornaceae"},
        )
