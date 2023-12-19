import unittest

from tests.setup import parse
from traiter.traiter.pylib.rules.utm import UTM


class TestUTMPatterns(unittest.TestCase):
    def test_utm_01(self):
        self.assertEqual(
            parse("""UTM: 12s 359602E 3718689N"""),
            [UTM(utm="12 S 359602 E 3718689 N", trait="utm", start=0, end=25)],
        )

    def test_utm_02(self):
        self.assertEqual(
            parse("""11UQF056380"""),
            [UTM(utm="11 UQF 056380", trait="utm", start=0, end=11)],
        )

    def test_utm_03(self):
        self.assertEqual(
            parse("""UTM 127 59000 E 4179660 N"""),
            [UTM(utm="127 59000 E 4179660 N", trait="utm", start=0, end=25)],
        )
