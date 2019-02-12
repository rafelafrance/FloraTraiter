# pylint: disable=missing-docstring,too-many-public-methods

import unittest
from lib.parse import Parse
from lib.traits.testes_size_trait import TestesSizeTrait


PAR = TestesSizeTrait()


class TestTestesSizeTrait(unittest.TestCase):

    def test_parse_01(self):
        self.assertEqual(
            PAR.parse('testes = 8x5 mm'),
            [Parse(value=[8, 5], units='mm', start=0, end=15)])

    def test_parse_02(self):
        self.assertEqual(
            PAR.parse('testes: 20mm. Sent to Berkeley 10/1/71'),
            [Parse(value=20, units='mm', start=0, end=12)])

    def test_parse_03(self):
        self.assertEqual(
            PAR.parse('ear from notch=19 mm; reproductive data=testis 5mm ; '),
            [Parse(value=5, units='mm', start=22, end=50)])

    def test_parse_04(self):
        self.assertEqual(
            PAR.parse('adult ; reproductive data=NS; T=9x4 ; endoparasite '),
            [Parse(value=[9, 4], units_inferred=True, start=8, end=35)])

    def test_parse_05(self):
        self.assertEqual(
            PAR.parse('2.3 g; reproductive data=testes: 18x8 mm; scrotal ;'),
            [Parse(value=[18, 8], units='mm', start=7, end=40)])

    def test_parse_06(self):
        self.assertEqual(
            PAR.parse('Plus Tissue; plus Baculum: Test 21x11'),
            [Parse(
                value=[21, 11],
                units_inferred=True,
                start=27, end=37)])

    def test_parse_07(self):
        self.assertEqual(
            PAR.parse('; reproductive data=testes scrotal; T = 9mm in length'),
            [Parse(value=9, units='mm', start=2, end=43)])

    def test_parse_08(self):
        self.assertEqual(
            PAR.parse('Scrotal 9 mm x 5 mm'),
            [Parse(value=[9, 5], units='mm', start=0, end=19)])

    def test_parse_09(self):
        self.assertEqual(
            PAR.parse('reproductive data=testes abdominal; T = 3 x 1.8 ;'),
            [Parse(
                value=[3, 1.8],
                units_inferred=True,
                start=0, end=47)])

    def test_parse_10(self):
        self.assertEqual(
            PAR.parse('testis-20mm ; reproductive data=testis-21mm ; '),
            [Parse(value=20, units='mm', start=0, end=11),
             Parse(value=21, units='mm', start=14, end=43)])

    def test_parse_11(self):
        self.assertEqual(
            PAR.parse('Testes x6'),
            [Parse(
                value=6,
                units_inferred=True,
                start=0, end=9)])

    def test_parse_12(self):
        self.assertEqual(
            #          0123456789 123456789 123456789 123456789
            PAR.parse('testes scrotal, L testis 13x5mm'),
            [Parse(value=[13, 5], units='mm', start=18, end=31)])

    def test_parse_13(self):
        self.assertEqual(
            PAR.parse('"gonad length 1":"3.0", "gonad length 2":"2.0",'),
            [Parse(value=3, units_inferred=True, side='1', dimension='length',
                   ambiguous_key=True, start=1, end=21),
             Parse(value=2, units_inferred=True, side='2', dimension='length',
                   ambiguous_key=True, start=25, end=45)])

    def test_parse_14(self):
        self.assertEqual(
            PAR.parse('"gonadLengthInMM":"12", "gonadWidthInMM":"5",'),
            [Parse(value=12, units='mm', ambiguous_key=True, dimension='length',
                   start=1, end=21),
             Parse(value=5, units='mm', ambiguous_key=True, dimension='width',
                   start=25, end=43)])

    def test_parse_15(self):
        self.assertEqual(
            PAR.parse('left gonad width=9.1 mm; right gonad width=9.2 mm; '
                      'right gonad length=16.1 mm; left gonad length=16.2 mm'),
            [Parse(value=9.1, units='mm', ambiguous_key=True, side='left',
                   dimension='width', start=0, end=23),
             Parse(value=9.2, units='mm', ambiguous_key=True, side='right',
                   dimension='width', start=25, end=49),
             Parse(value=16.1, units='mm', ambiguous_key=True, side='right',
                   dimension='length', start=51, end=77),
             Parse(value=16.2, units='mm', ambiguous_key=True, side='left',
                   dimension='length', start=79, end=104)])

    def test_parse_16(self):
        self.assertEqual(
            PAR.parse('"gonadLengthInMM":"9mm w.o./epid", '),
            [Parse(value=9, units='mm', ambiguous_key=True, dimension='length',
                   start=1, end=22)])

    def test_parse_17(self):
        self.assertEqual(
            PAR.parse('testis-7mm'),
            [Parse(value=7, units='mm', start=0, end=10)])

    def test_parse_18(self):
        self.assertEqual(
            PAR.parse('reproductive data=T=10x4 ; '),
            [Parse(value=[10, 4], units_inferred=True, start=0, end=24)])

    def test_parse_19(self):
        self.assertEqual(
            PAR.parse(
                'x=male ; reproductive data=testes abdominal ; '
                'weight=30 g; hind foot with claw=32 mm; ear from '
                'notch=28 mm; tail length=89 mm; unformatted '
                'measurements=196-89-32-28=30 ; total length=196 mm'),
            [])

    def test_parse_20(self):
        self.assertEqual(
            PAR.parse('adult ; T=9x4 ; endoparasite '),
            [Parse(value=[9, 4], units_inferred=True, ambiguous_key=True,
                   start=8, end=13)])

    def test_parse_21(self):
        self.assertEqual(
            PAR.parse('adult ; T=9 ; endoparasite '),
            [])

    def test_parse_22(self):
        self.assertEqual(
            PAR.parse('TESTES 5-3.5 MM,'),
            [Parse(value=[5, 3.5], units='mm', start=0, end=15)])

    def test_parse_23(self):
        self.assertEqual(
            PAR.parse('reproductive data=T: R-2x4mm ; '),
            [Parse(value=[2, 4], units='mm', side='r',
                   start=0, end=28)])

    def test_parse_24(self):
        self.assertEqual(
            PAR.parse('reproductive data=T: L-2x4mm ; '),
            [Parse(value=[2, 4], units='mm', side='l',
                   start=0, end=28)])

    def test_parse_25(self):
        self.assertEqual(
            PAR.parse('testes (R) 6 x 1.5 & 5 x 2 mm'),
            [Parse(value=[6, 1.5], units_inferred=True, side='r',
                   start=0, end=18)])

    def test_parse_26(self):
        self.assertEqual(
            PAR.parse('Cataloged by: R.L. Humphrey, 31 January 1995'),
            [])

    def test_parse_27(self):
        self.assertEqual(
            PAR.parse('; reproductive data=5x3 inguinal ;'),
            [Parse(value=[5, 3], units_inferred=True,
                   start=2, end=23)])

    def test_parse_28(self):
        self.assertEqual(
            PAR.parse("sex=male ; reproductive data=Testes .5' , scrotal"),
            [Parse(value=152.4, units="'", start=11, end=39)])