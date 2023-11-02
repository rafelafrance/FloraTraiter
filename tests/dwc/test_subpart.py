import unittest

from tests.setup import to_dwc

LABEL = "subpart"


class TestSubpart(unittest.TestCase):
    def test_subpart_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "male leaf teeth"),
            {"dwc:dynamicProperties": {"maleLeafTeeth": "leaf teeth"}},
        )

    def test_subpart_dwc_02(self):
        self.assertEqual(
            to_dwc(LABEL, "Missing leaf teeth"),
            {"dwc:dynamicProperties": {"missingLeafTeeth": "missing leaf teeth"}},
        )
