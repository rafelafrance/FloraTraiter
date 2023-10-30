import unittest

from tests.setup import to_ent

LABEL = "reproduction"


class TestReproduction(unittest.TestCase):
    def test_reproduction_dwc_01(self):
        ent = to_ent(LABEL, "gynodioecious")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dynamicProperties": {"reproduction": "gynodioecious"}}
        )
