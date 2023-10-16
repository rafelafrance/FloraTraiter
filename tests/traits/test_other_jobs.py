import unittest

from tests.setup import full_test


class TestOtherJob(unittest.TestCase):
    def test_other_job_01(self):
        """It gets a job notation."""
        self.assertEqual(
            full_test("""Verified by: John Kinsman:"""),
            [
                {
                    "name": "John Kinsman",
                    "job": "verified by",
                    "trait": "job",
                    "start": 0,
                    "end": 25,
                }
            ],
        )
