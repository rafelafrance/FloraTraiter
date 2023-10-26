import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "part"


class TestPart(unittest.TestCase):
    def test_part_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "with thick, woody rootstock.")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"plantPart": "rootstock"}})
