import unittest

from tests.setup import to_ent

LABEL = "part_location"


class TestPartLocation(unittest.TestCase):
    def test_part_location_dwc_01(self):
        ent = to_ent(LABEL, "adnate to petiole for 1-2 mm")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {"dynamicProperties": {"partAsDistance": "adnate to petiole for 1 - 2 mm"}},
        )
