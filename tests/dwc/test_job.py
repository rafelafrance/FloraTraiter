import unittest

from tests.setup import to_ent

LABEL = "job"


class TestJob(unittest.TestCase):
    def test_job_01(self):
        ent = to_ent(LABEL, "Sarah Nunn and S. Jacobs and R. Mc Elderry 9480")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:dynamicProperties": {
                    "collector": "Sarah Nunn, S. Jacobs, R. Mc Elderry",
                    "collectorIdNumber": "9480",
                },
            },
        )

    def test_job_02(self):
        ent = to_ent(LABEL, "Det;; N. H Russell 195")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:dynamicProperties": {
                    "determiner": "N. H Russell",
                    "determinerIdNumber": "195",
                },
            },
        )

    def test_job_03(self):
        ent = to_ent(LABEL, "Verified by: John Kinsman:")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(), {"dwc:dynamicProperties": {"verifier": "John Kinsman"}}
        )

    def test_job_04(self):
        ent = to_ent(LABEL, "With: Dawn Goldman, Army Prince")
        dwc = ent._.trait.to_dwc(ent)
        self.assertEqual(
            dwc.to_dict(),
            {
                "dwc:dynamicProperties": {
                    "otherCollector": "Dawn Goldman, Army Prince"
                },
            },
        )
