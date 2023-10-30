import unittest

from tests.setup import to_ent

LABEL = "duration"


class TestDuration(unittest.TestCase):
    def test_duration_dwc_01(self):
        ent = to_ent(LABEL, "juvenile leaves persistent for a long period.")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dynamicProperties": {"leafDuration": "persistent"}}
        )
