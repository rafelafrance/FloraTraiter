import unittest

from flora.pylib.rules.taxon import Taxon
from flora.pylib.rules.taxon_like import TaxonLike
from flora.pylib.rules.venation import Venation
from tests.setup import parse


class TestTaxonLike(unittest.TestCase):
    def test_taxon_like_01(self):
        self.assertEqual(
            parse("""it seems closer to the nearly sympatric M. sensitiva."""),
            [
                TaxonLike(
                    taxon_like="Mimosa sensitiva",
                    trait="taxon_like",
                    start=30,
                    end=52,
                    relation="sympatric",
                )
            ],
        )

    def test_taxon_like_02(self):
        self.assertEqual(
            parse("""it is similar to M. sensitiva."""),
            [
                TaxonLike(
                    taxon_like="Mimosa sensitiva",
                    trait="taxon_like",
                    start=6,
                    end=29,
                    relation="similar",
                )
            ],
        )

    def test_taxon_like_03(self):
        self.assertEqual(
            parse("""It resembles M. sensitiva in amplitude"""),
            [
                TaxonLike(
                    taxon_like="Mimosa sensitiva",
                    trait="taxon_like",
                    start=3,
                    end=25,
                    relation="resembles",
                )
            ],
        )

    def test_taxon_like_04(self):
        self.assertEqual(
            parse("""sympatric pair of M. sensitiva Harms ex Glaziou"""),
            [
                TaxonLike(
                    taxon_like="Mimosa sensitiva",
                    trait="taxon_like",
                    start=0,
                    end=47,
                    relation="sympatric",
                )
            ],
        )

    def test_taxon_like_05(self):
        self.assertEqual(
            parse("""vicinis M. sensitiva et A. pachyphloia"""),
            [
                TaxonLike(
                    taxon_like=["Mimosa sensitiva", "Acacia pachyphloia"],
                    trait="taxon_like",
                    start=0,
                    end=38,
                    relation="vicinis",
                )
            ],
        )

    def test_taxon_like_06(self):
        self.assertEqual(
            parse("""distinguished from var. pachyphloia"""),
            [
                TaxonLike(
                    trait="taxon_like",
                    start=0,
                    end=35,
                    taxon_like="pachyphloia",
                    relation="distinguished",
                )
            ],
        )

    def test_taxon_like_07(self):
        self.assertEqual(
            parse("""The var. floridana resembles var. nuttallii in venation"""),
            [
                Taxon(
                    rank="variety",
                    taxon="floridana",
                    trait="taxon",
                    start=4,
                    end=18,
                    taxon_like="nuttallii",
                    associated=True,
                ),
                TaxonLike(
                    trait="taxon_like",
                    start=19,
                    end=43,
                    taxon_like="nuttallii",
                    relation="resembles",
                ),
                Venation(venation="vein", trait="venation", start=47, end=55),
            ],
        )
