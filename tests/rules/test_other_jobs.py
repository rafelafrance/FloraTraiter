import unittest

from flora.pylib.rules.job import Job
from tests.setup import parse


class TestOtherJob(unittest.TestCase):
    def test_other_job_01(self):
        """It gets a job notation."""
        self.assertEqual(
            parse("""Verified by: John Kinsman:"""),
            [
                Job(
                    name="John Kinsman",
                    job="verifier",
                    trait="job",
                    start=0,
                    end=25,
                    has_label=True,
                )
            ],
        )
