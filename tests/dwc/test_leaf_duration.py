import unittest

from tests.setup import to_dwc

LABEL = "leaf_duration"


class TestLeafDuration(unittest.TestCase):
    def test_leaf_duration_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "deciduous"),
            {"dwc:dynamicProperties": {"leafDuration": "deciduous"}},
        )
