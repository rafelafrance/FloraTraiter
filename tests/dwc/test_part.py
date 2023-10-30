import unittest

from tests.setup import to_ent

LABEL = "part"


class TestPart(unittest.TestCase):
    def test_part_dwc_01(self):
        ent = to_ent(LABEL, "with thick, woody rootstock.")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"plantPart": "rootstock"}}
        )
