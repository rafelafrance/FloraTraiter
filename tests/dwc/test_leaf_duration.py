import unittest

from tests.setup import to_ent

LABEL = "leaf_duration"


class TestLeafDuration(unittest.TestCase):
    def test_leaf_duration_dwc_01(self):
        ent = to_ent(LABEL, "deciduous")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dynamicProperties": {"leafDuration": "deciduous"}}
        )
