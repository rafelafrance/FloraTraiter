import unittest

from tests.setup import PIPELINE
from traiter.pylib.pipes import tokenizer


class TestTokenizer(unittest.TestCase):
    def test_remove_special_case_01(self):
        special = [r for r in PIPELINE.tokenizer.rules if r == "Jan."]
        self.assertEqual(special, ["Jan."])

        tokenizer.remove_special_case(PIPELINE, ["Jan."])
        special = [r for r in PIPELINE.tokenizer.rules if r == "Jan."]
        self.assertEqual(special, [])
