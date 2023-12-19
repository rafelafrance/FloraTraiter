import unittest

from tests.setup import PIPELINE
from traiter.traiter.pylib.util import shorten


class TestSentence(unittest.TestCase):
    def test_sentencizer_01(self):
        text = shorten("""It was common “along a tiny stream.” Argia apicalis.""")
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 2)

    def test_sentencizer_02(self):
        text = shorten("""(Dunn et al. 2009, Jørgensen 2015).""")
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 1)

    def test_sentencizer_03(self):
        text = """Abbreviated
            when
            subsequently mentioned."""
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 1)

    def test_sentencizer_04(self):
        text = """Up to 3 mm. Sometimes blue."""
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 2)

    def test_sentencizer_05(self):
        text = shorten(
            """
            Plants perennial (rhizomatous), usually glabrous, sometimes sparsely hairy.
            Stems [10–]30–70[–100] cm. Leaves: stipules lanceolate to oblong.
            """
        )
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 3)

    def test_sentencizer_06(self):
        text = shorten(
            """
            Capsules 8–15 × 6–12 mm, larger wings deltate-rounded, 10–17 mm wide,
            smaller 3.5–5 mm wide. 2n = 34, 56 (South America).
            """
        )
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 2)

    def test_sentencizer_07(self):
        text = shorten("""Ciald., Darwiniana.""")
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 1)

    def test_sentencizer_08(self):
        text = shorten("""(e.g. 1. carinata, Fig. 231).""")
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 1)

    def test_sentencizer_09(self):
        text = shorten("""I""")
        doc = PIPELINE(text)
        sents = list(doc.sents)
        self.assertEqual(len(sents), 1)
