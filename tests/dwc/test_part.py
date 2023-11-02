import unittest

from tests.setup import to_dwc

LABEL = "part"


class TestPart(unittest.TestCase):
    def test_part_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "with thick, woody rootstock."),
            {"dwc:dynamicProperties": {"plantPart": "rootstock"}},
        )
