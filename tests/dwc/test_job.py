import unittest

from tests.setup import to_dwc

LABEL = "job"


class TestJob(unittest.TestCase):
    def test_job_01(self):
        self.assertEqual(
            to_dwc(LABEL, "Sarah Nunn and S. Jacobs and R. Mc Elderry 9480"),
            {
                "dwc:recordedBy": "Sarah Nunn | S. Jacobs | R. Mc Elderry",
            },
        )

    def test_job_02(self):
        self.assertEqual(
            to_dwc(LABEL, "Det;; N. H Russell 195"),
            {
                "dwc:identifiedBy": "N. H Russell",
            },
        )

    def test_job_03(self):
        self.assertEqual(
            to_dwc(LABEL, "Verified by: John Kinsman:"),
            {"dwc:dynamicProperties": {"verifier": "John Kinsman"}},
        )

    def test_job_04(self):
        self.assertEqual(
            to_dwc(LABEL, "With: Dawn Goldman, Army Prince"),
            {"dwc:recordedBy": "Dawn Goldman | Army Prince"},
        )
