import unittest

from tests.setup import to_dwc

LABEL = "id_number"


class TestJob(unittest.TestCase):
    def test_job_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Sarah Nunn and S. Jacobs and R. Mc Elderry 9480"),
            {
                "dwc:recordNumber": "9480",
            },
        )

    def test_job_02(self):
        self.assertEqual(
            to_dwc(LABEL, "Det;; N. H Russell 195"),
            {
                "dwc:recordNumber": "195",
            },
        )
