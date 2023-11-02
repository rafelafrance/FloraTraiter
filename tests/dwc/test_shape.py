import unittest

from tests.setup import to_dwc

LABEL = "shape"


class TestShape(unittest.TestCase):
    def test_shape_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "leaf suborbiculate"),
            {"dwc:dynamicProperties": {"leafShape": "orbicular"}},
        )
