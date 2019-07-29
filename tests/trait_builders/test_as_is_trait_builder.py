import unittest
from traiter.trait import Trait
from traiter.trait_builders.as_is_trait_builder import AsIsTraitBuilder


PAR = None


class TestAsIsTraitBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global PAR
        PAR = AsIsTraitBuilder()

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('word'),
            [Trait(value='word', as_is=True, start=0, end=4)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse(' word  '),
            [Trait(value='word', as_is=True, start=1, end=5)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse(' x  '),
            [Trait(value='x', as_is=True, start=1, end=2)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('x'),
            [Trait(value='x', as_is=True, start=0, end=1)])

    def test_parse_05(self):
        self.assertEqual(PAR.parse(''), [])

    def test_parse_06(self):
        self.assertEqual(PAR.parse('  '), [])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse(' word  word '),
            [Trait(value='word  word', as_is=True, start=1, end=11)])