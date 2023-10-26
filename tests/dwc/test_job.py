import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "job"


class TestJob(unittest.TestCase):
    def test_job_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Sarah Nunn and S. Jacobs and R. Mc Elderry 9480")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {
                    "collector": "Sarah Nunn, S. Jacobs, R. Mc Elderry",
                    "collectorIdNumber": "9480",
                },
            },
        )

    def test_job_02(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Det;; N. H Russell 195")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {
                    "determiner": "N. H Russell",
                    "determinerIdNumber": "195",
                },
            },
        )

    def test_job_03(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "Verified by: John Kinsman:")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"verifier": "John Kinsman"}})

    def test_job_04(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "With: Dawn Goldman, Army Prince")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(
            actual,
            {
                "dynamicProperties": {"otherCollector": "Dawn Goldman, Army Prince"},
            },
        )
