import unittest

from flora.pylib.rules.part import Part
from flora.pylib.rules.taxon import Taxon
from tests.setup import parse


class TestTaxon(unittest.TestCase):
    def test_taxon_01(self):
        self.assertEqual(
            parse("""M. sensitiva"""),
            [
                Taxon(
                    rank="species",
                    taxon="Mimosa sensitiva",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_taxon_02(self):
        self.assertEqual(
            parse("""Mimosa sensitiva"""),
            [
                Taxon(
                    rank="species",
                    taxon="Mimosa sensitiva",
                    start=0,
                    end=16,
                ),
            ],
        )

    def test_taxon_03(self):
        self.assertEqual(
            parse("""M. polycarpa var. spegazzinii"""),
            [
                Taxon(
                    rank="variety",
                    taxon="M. polycarpa var. spegazzinii",
                    start=0,
                    end=29,
                ),
            ],
        )

    def test_taxon_04(self):
        self.assertEqual(
            parse("""A. pachyphloia subsp. brevipinnula."""),
            [
                Taxon(
                    rank="subspecies",
                    taxon="Acacia pachyphloia subsp. brevipinnula",
                    start=0,
                    end=34,
                ),
            ],
        )

    def test_taxon_05(self):
        self.assertEqual(
            parse("""A. pachyphloia Bamehy 184."""),
            [
                Taxon(
                    rank="species",
                    taxon="Acacia pachyphloia",
                    authority="Bamehy",
                    start=0,
                    end=21,
                ),
            ],
        )

    def test_taxon_06(self):
        self.assertEqual(
            parse("""A. pachyphloia Britton & Rose"""),
            [
                Taxon(
                    authority="Britton and Rose",
                    rank="species",
                    taxon="Acacia pachyphloia",
                    start=0,
                    end=29,
                ),
            ],
        )

    def test_taxon_07(self):
        self.assertEqual(
            parse("""Ser. Vulpinae is characterized"""),
            [
                Taxon(
                    rank="series",
                    taxon="Vulpinae",
                    start=0,
                    end=13,
                ),
            ],
        )

    def test_taxon_08(self):
        self.assertEqual(
            parse("""All species are trees"""),
            [Part(end=21, part="tree", start=16, type="plant_part")],
        )

    def test_taxon_09(self):
        self.assertEqual(
            parse("""Alajuela, between La Palma and Rio Platanillo"""),
            [],
        )

    def test_taxon_10(self):
        self.assertEqual(
            parse("""together with A. pachyphloia (Vulpinae)"""),
            [
                Taxon(
                    taxon="Acacia pachyphloia",
                    rank="species",
                    start=14,
                    end=28,
                ),
                Taxon(
                    taxon="Vulpinae",
                    rank="section",
                    start=30,
                    end=38,
                ),
            ],
        )

    def test_taxon_11(self):
        self.assertEqual(
            parse("""Mimosa sensitiva (Bentham) Fox, Trans."""),
            [
                Taxon(
                    authority="Bentham Fox",
                    rank="species",
                    taxon="Mimosa sensitiva",
                    start=0,
                    end=31,
                ),
            ],
        )

    def test_taxon_12(self):
        self.assertEqual(
            parse(
                """
                Neptunia gracilis f. gracilis Neptunia gracilis var. villosula Benth.,
                """,
            ),
            [
                Taxon(
                    taxon="Neptunia gracilis f. gracilis",
                    rank="form",
                    start=0,
                    end=29,
                ),
                Taxon(
                    taxon="Neptunia gracilis var. villosula",
                    rank="variety",
                    authority="Benth",
                    start=30,
                    end=69,
                ),
            ],
        )

    def test_taxon_13(self):
        """It handles 'F.' genus abbreviation vs 'f.' form abbreviation."""
        self.assertEqual(
            parse(
                """
                F. gracilis Neptunia gracilis var. villosula Benth.,
                """,
            ),
            [
                Taxon(
                    taxon="F. gracilis",
                    rank="species",
                    start=0,
                    end=11,
                ),
                Taxon(
                    taxon="Neptunia gracilis var. villosula",
                    rank="variety",
                    authority="Benth",
                    start=12,
                    end=51,
                ),
            ],
        )

    def test_taxon_14(self):
        self.assertEqual(
            parse("""Ticanto rhombifolia"""),
            [
                Taxon(
                    taxon="Ticanto rhombifolia",
                    rank="species",
                    start=0,
                    end=19,
                ),
            ],
        )

    def test_taxon_15(self):
        """It gets a taxon notation."""
        self.assertEqual(
            parse(
                """
                Cornaceae
                Cornus obliqua Raf.
                """,
            ),
            [
                Taxon(
                    rank="family",
                    taxon="Cornaceae",
                    start=0,
                    end=9,
                ),
                Taxon(
                    authority="Raf",
                    rank="species",
                    taxon="Cornus obliqua",
                    start=10,
                    end=29,
                ),
            ],
        )

    def test_taxon_16(self):
        """It gets a family notation."""
        self.assertEqual(
            parse(
                """
                Crowley's Ridge
                Fabaceae
                Vicia villosa Roth ssp. varia (Khan)
                """,
            ),
            [
                Taxon(
                    taxon="Fabaceae",
                    rank="family",
                    start=16,
                    end=24,
                ),
                Taxon(
                    taxon="Vicia villosa subsp. varia",
                    rank="subspecies",
                    authority=["Roth", "Khan"],
                    start=25,
                    end=61,
                ),
            ],
        )

    def test_taxon_17(self):
        """It gets the full notation."""
        self.assertEqual(
            parse("""Cephalanthus occidentalis L. Rubiaceas"""),
            [
                Taxon(
                    taxon="Cephalanthus occidentalis",
                    rank="species",
                    authority="L. Rubiaceas",
                    start=0,
                    end=38,
                ),
            ],
        )

    def test_taxon_18(self):
        """It handles 'f.' form abbreviation vs 'F.' genus abbreviation."""
        self.assertEqual(
            parse("""A. pachyphloia f. brevipinnula."""),
            [
                Taxon(
                    rank="form",
                    taxon="Acacia pachyphloia f. brevipinnula",
                    start=0,
                    end=30,
                ),
            ],
        )

    def test_taxon_19(self):
        """Do not maximize the authority."""
        self.assertEqual(
            parse(
                """Cornus obliqua Willd.
                In Fraijanes Recreation Park""",
            ),
            [
                Taxon(
                    taxon="Cornus obliqua",
                    rank="species",
                    authority="Willd",
                    start=0,
                    end=21,
                ),
            ],
        )

    def test_taxon_20(self):
        """It gets an all caps monomial."""
        self.assertEqual(
            parse("""PLANTS OF PENNSYLVANIA ASTERACEAE"""),
            [
                Taxon(
                    taxon="Asteraceae",
                    rank="family",
                    start=23,
                    end=33,
                ),
            ],
        )

    def test_taxon_21(self):
        self.assertEqual(
            parse("""Mimosa sensitiva (L.) Fox, Trans."""),
            [
                Taxon(
                    authority="Linnaeus, Fox",
                    rank="species",
                    taxon="Mimosa sensitiva",
                    start=0,
                    end=26,
                ),
            ],
        )

    def test_taxon_22(self):
        self.assertEqual(
            parse(
                """
                Cephalanthus occidentalis L. Rubiaceas
                Associated species: Cornus obliqua
                """,
            ),
            [
                Taxon(
                    taxon="Cephalanthus occidentalis",
                    rank="species",
                    authority="L. Rubiaceas",
                    start=0,
                    end=38,
                ),
                Taxon(
                    taxon="Cornus obliqua",
                    rank="species",
                    start=59,
                    end=73,
                ),
            ],
        )

    def test_taxon_23(self):
        self.assertEqual(
            parse("""Mimosa sensitiva (L.) subsp. varia Fox."""),
            [
                Taxon(
                    authority=["Linnaeus", "Fox"],
                    rank="subspecies",
                    taxon="Mimosa sensitiva subsp. varia",
                    start=0,
                    end=39,
                ),
            ],
        )

    def test_taxon_24(self):
        self.assertEqual(
            parse("""Mimosa sensitiva (R. Person) subsp. varia Fox."""),
            [
                Taxon(
                    authority=["R. Person", "Fox"],
                    rank="subspecies",
                    taxon="Mimosa sensitiva subsp. varia",
                    start=0,
                    end=46,
                ),
            ],
        )

    def test_taxon_25(self):
        self.assertEqual(
            parse("""Mimosa sensitiva (L. Person) subsp. varia Fox."""),
            [
                Taxon(
                    authority=["L. Person", "Fox"],
                    rank="subspecies",
                    taxon="Mimosa sensitiva subsp. varia",
                    start=0,
                    end=46,
                ),
            ],
        )

    def test_taxon_26(self):
        """It handles a taxon next to a name with a trailing ID number."""
        self.maxDiff = None
        self.assertEqual(
            parse("""Associated species: Neptunia gracilis G. Rink 7075"""),
            [
                Taxon(
                    start=20,
                    end=37,
                    _text="Neptunia gracilis",
                    taxon="Neptunia gracilis",
                    rank="species",
                ),
            ],
        )

    def test_taxon_27(self):
        self.maxDiff = None
        self.assertEqual(
            parse(""" Name Neptunia gracilis Geyser Locality Vernal, """),
            [
                Taxon(
                    authority="Geyser",
                    taxon="Neptunia gracilis",
                    rank="species",
                    start=5,
                    end=29,
                ),
            ],
        )

    def test_taxon_28(self):
        self.assertEqual(
            parse(""" Neptunia gracilis (Gray) """),
            [
                Taxon(
                    authority="Gray",
                    taxon="Neptunia gracilis",
                    rank="species",
                    start=0,
                    end=24,
                ),
            ],
        )

    def test_taxon_29(self):
        self.assertEqual(
            parse("""Neptunia gracilis & Mimosa sensitiva"""),
            [
                Taxon(
                    rank="species",
                    taxon=["Neptunia gracilis", "Mimosa sensitiva"],
                    start=0,
                    end=36,
                ),
            ],
        )

    def test_taxon_30(self):
        self.assertEqual(
            parse("""Neptunia gracilis (Roxb.) T. Anderson"""),
            [
                Taxon(
                    authority="Roxb T. Anderson",
                    rank="species",
                    taxon="Neptunia gracilis",
                    start=0,
                    end=37,
                ),
            ],
        )

    def test_taxon_31(self):
        self.assertEqual(
            parse("""Quercus/Cytisus/Agrostis"""),
            [
                Taxon(
                    taxon="Quercus",
                    rank="genus",
                    start=0,
                    end=7,
                ),
                Taxon(
                    taxon="Cytisus",
                    rank="genus",
                    start=8,
                    end=15,
                ),
                Taxon(
                    taxon="Agrostis",
                    rank="genus",
                    start=16,
                    end=24,
                ),
            ],
        )

    def test_taxon_32(self):
        self.assertEqual(
            parse("""Neptunia gracilis Muhl. ex Willd. var. varia (Nutt.) Brewer"""),
            [
                Taxon(
                    taxon="Neptunia gracilis var. varia",
                    rank="variety",
                    start=0,
                    end=59,
                    authority=["Muhl and Willd", "Nutt", "Brewer"],
                ),
            ],
        )

    def test_taxon_33(self):
        self.assertEqual(
            parse("""Neptunia gracilis (L.) Pers."""),
            [
                Taxon(
                    taxon="Neptunia gracilis",
                    rank="species",
                    start=0,
                    end=28,
                    authority="Linnaeus, Pers",
                ),
            ],
        )

    def test_taxon_34(self):
        self.assertEqual(
            parse("""Neptunia gracilis v.Varia by G. McPherson, confirmed Vink"""),
            [
                Taxon(
                    taxon="Neptunia gracilis var. varia",
                    rank="variety",
                    start=0,
                    end=42,
                    authority="G. McPherson",
                ),
            ],
        )

    def test_taxon_35(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                "Neptunia gracilis (Torr. & A. Gray ex A. Gray) W.A. Weber & A. Love",
            ),
            [
                Taxon(
                    taxon="Neptunia gracilis",
                    rank="species",
                    start=0,
                    end=67,
                    authority="Torr and A. Gray and A. Gray W. A. Weber and A. Love",
                ),
            ],
        )

    def test_taxon_36(self):
        self.assertEqual(
            parse(
                """
                Neptunia gracilis (Heller) Chuang & Heckard
                ssp. varia (Heller) Chuang & Heckard
                """,
            ),
            [
                Taxon(
                    taxon="Neptunia gracilis subsp. varia",
                    rank="subspecies",
                    start=0,
                    end=80,
                    authority=[
                        "Heller Chuang and Heckard",
                        "Heller",
                        "Chuang",
                        "Heckard",
                    ],
                ),
            ],
        )

    def test_taxon_37(self):
        self.assertEqual(
            parse("""Neptunia gracilis var. varia (A. Gray) N.H. Holmgren,"""),
            [
                Taxon(
                    taxon="Neptunia gracilis var. varia",
                    rank="variety",
                    start=0,
                    end=53,
                    authority="A. Gray N.H. Holmgren",
                ),
            ],
        )

    # def test_taxon_38(self):
    #     self.assertEqual(
    #         parse("""
    #             Lupinus arizonicus Douglas ex Hooker
    #             ssp. gracilis (C. P. Smith) Conrad
    #             var. varia (S. Watson) Conrad"""),
    #         [
    #             Taxon(
    #                 taxon="Neptunia gracilis",
    #                 rank="variety",
    #                 start=0,
    #                 end=35,
    #                 authority="Douglas and Hooker",
    #             ),
    #         ],
    #     )
