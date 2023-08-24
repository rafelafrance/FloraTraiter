import unittest

from tests.setup import test2


class TestOtherJob(unittest.TestCase):
    def test_other_job_01(self):
        """It gets a job notation."""
        self.assertEqual(
            test2("""Verified by: John Kinsman:"""),
            [
                {
                    "worker": "John Kinsman",
                    "job": "verified by",
                    "trait": "other_job",
                    "start": 0,
                    "end": 25,
                }
            ],
        )
