"""Test the spell checker."""
import unittest

from traiter.traiter.pylib.spell_well import SpellWell


class TestSpellWell(unittest.TestCase):
    spell_well = SpellWell()

    def test_correct_01(self):
        self.assertEqual(self.spell_well.correct("Missing"), "Missing")

    def test_correct_02(self):
        self.assertEqual(self.spell_well.correct(None), "")

    def test_correct_03(self):
        self.assertEqual(self.spell_well.correct("abdome"), "abdomen")

    def test_correct_04(self):
        self.assertEqual(self.spell_well.correct("abdoman"), "abdomen")

    def test_freq_01(self):
        self.assertEqual(self.spell_well.freq("acaulescent"), 1035)

    def test_freq_02(self):
        self.assertEqual(self.spell_well.freq("zebra"), 20687)
