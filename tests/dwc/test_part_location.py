import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "part_location"


class TestPartLocation(unittest.TestCase):
    def test_part_location_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "adnate to petiole for 1-2 mm")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {"dynamicProperties": {"partAsDistance": "adnate to petiole for 1 - 2 mm"}},
        )
