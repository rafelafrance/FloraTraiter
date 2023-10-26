import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "admin_unit"


class TestAdminUnit(unittest.TestCase):
    def test_admin_unit_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Flora of ARKANSAS County: MISSISSIPPI")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"stateProvince": "Arkansas", "county": "Mississippi"})

    def test_admin_unit_dwc_02(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "The University of Georgia Athens, GA, U.S.A.")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"country": "USA"})

    def test_admin_unit_dwc_03(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Province of Panama")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"stateProvince": "panama"})
