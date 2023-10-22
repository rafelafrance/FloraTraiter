import unittest

from flora.pylib.traits.job import Job
from tests.setup import test


class TestOtherJob(unittest.TestCase):
    def test_other_job_01(self):
        """It gets a job notation."""
        self.assertEqual(
            test("""Verified by: John Kinsman:"""),
            [
                Job(
                    name="John Kinsman",
                    job="verifier",
                    trait="job",
                    start=0,
                    end=25,
                )
            ],
        )
