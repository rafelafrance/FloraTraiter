import unittest

from tests.setup import to_dwc

LABEL = "duration"


class TestDuration(unittest.TestCase):
    def test_duration_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "juvenile leaves persistent for a long period."),
            {"dwc:dynamicProperties": {"leafDuration": "persistent"}},
        )
