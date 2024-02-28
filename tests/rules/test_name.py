import unittest

from tests.setup import parse


class TestName(unittest.TestCase):
    def test_name_01(self):
        """It should skip this."""
        self.assertEqual(
            parse("San Benito County, California."),
            [],
        )
