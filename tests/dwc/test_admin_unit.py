import unittest

from tests.setup import to_dwc

LABEL = "admin_unit"


class TestAdminUnit(unittest.TestCase):
    def test_admin_unit_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Flora of ARKANSAS County: MISSISSIPPI"),
            {"dwc:stateProvince": "Arkansas", "dwc:county": "Mississippi"},
        )

    def test_admin_unit_dwc_02(self):
        self.assertEqual(
            to_dwc(LABEL, "The University of Georgia Athens, GA, U.S.A."),
            {"dwc:country": "USA"},
        )

    def test_admin_unit_dwc_03(self):
        self.assertEqual(
            to_dwc(LABEL, "Province of Panama"), {"dwc:stateProvince": "panama"}
        )
