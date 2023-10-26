import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "reproduction"


class TestReproduction(unittest.TestCase):
    def test_reproduction_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "gynodioecious")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual, {"dynamicProperties": {"reproduction": "gynodioecious"}}
        )
