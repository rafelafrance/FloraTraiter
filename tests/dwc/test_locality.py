import unittest

from tests.setup import to_dwc

LABEL = "locality"


class TestLocality(unittest.TestCase):
    def test_locality_dwc_01(self):
        verb = "5 miles North of Mason off Hwy 386."
        self.assertEqual(to_dwc(LABEL, verb), {"dwc:verbatimLocality": verb})
