import unittest

from tests.setup import to_dwc

LABEL = "date"


class TestDate(unittest.TestCase):
    def test_date_dwc_01(self):
        self.assertEqual(
            to_dwc(LABEL, "14 JAN. 1987"),
            {"dwc:eventDate": "1987-01-14", "dwc:verbatimEventDate": "14 JAN. 1987"},
        )
