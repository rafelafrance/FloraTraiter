import unittest

from tests.setup import to_ent

LABEL = "admin_unit"


class TestAdminUnit(unittest.TestCase):
    def test_admin_unit_dwc_01(self):
        ent = to_ent(LABEL, "Flora of ARKANSAS County: MISSISSIPPI")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {"dwc:stateProvince": "Arkansas", "dwc:county": "Mississippi"},
        )

    def test_admin_unit_dwc_02(self):
        ent = to_ent(LABEL, "The University of Georgia Athens, GA, U.S.A.")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(dwc.to_dict(), {"dwc:country": "USA"})

    def test_admin_unit_dwc_03(self):
        ent = to_ent(LABEL, "Province of Panama")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(dwc.to_dict(), {"dwc:stateProvince": "panama"})
