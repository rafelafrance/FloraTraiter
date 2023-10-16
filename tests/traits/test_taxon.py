import unittest

from tests.setup import full_test
from tests.setup import small_test


class TestTaxon(unittest.TestCase):
    def test_taxon_00(self):
        small_test("""Cornus obliqua (Beth.)""")

    def test_taxon_01(self):
        self.assertEqual(
            small_test("""M. sensitiva"""),
            [
                {
                    "rank": "species",
                    "taxon": "Mimosa sensitiva",
                    "trait": "taxon",
                    "start": 0,
                    "end": 12,
                }
            ],
        )

    def test_taxon_02(self):
        self.assertEqual(
            small_test("""Mimosa sensitiva"""),
            [
                {
                    "rank": "species",
                    "taxon": "Mimosa sensitiva",
                    "trait": "taxon",
                    "start": 0,
                    "end": 16,
                }
            ],
        )

    def test_taxon_03(self):
        self.assertEqual(
            small_test("""M. polycarpa var. spegazzinii"""),
            [
                {
                    "rank": "variety",
                    "taxon": "M. polycarpa var. spegazzinii",
                    "trait": "taxon",
                    "start": 0,
                    "end": 29,
                }
            ],
        )

    def test_taxon_04(self):
        self.assertEqual(
            small_test("""A. pachyphloia subsp. brevipinnula."""),
            [
                {
                    "rank": "subspecies",
                    "taxon": "Acacia pachyphloia subsp. brevipinnula",
                    "trait": "taxon",
                    "start": 0,
                    "end": 34,
                }
            ],
        )

    def test_taxon_05(self):
        self.assertEqual(
            small_test("""A. pachyphloia Bamehy 184."""),
            [
                {
                    "rank": "species",
                    "taxon": "Acacia pachyphloia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 14,
                }
            ],
        )

    def test_taxon_06(self):
        self.assertEqual(
            small_test("""A. pachyphloia Britton & Rose"""),
            [
                {
                    "authority": "Britton and Rose",
                    "rank": "species",
                    "taxon": "Acacia pachyphloia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 29,
                }
            ],
        )

    def test_taxon_07(self):
        self.assertEqual(
            small_test("""Ser. Vulpinae is characterized"""),
            [
                {
                    "rank": "series",
                    "taxon": "Vulpinae",
                    "trait": "taxon",
                    "start": 0,
                    "end": 13,
                }
            ],
        )

    def test_taxon_08(self):
        self.assertEqual(
            small_test("""All species are trees"""),
            [{"end": 21, "plant_part": "tree", "start": 16, "trait": "plant_part"}],
        )

    def test_taxon_09(self):
        self.assertEqual(
            small_test("""Alajuela, between La Palma and Rio Platanillo"""),
            [],
        )

    def test_taxon_10(self):
        self.assertEqual(
            small_test("""together with A. pachyphloia (Vulpinae)"""),
            [
                {
                    "taxon": "Acacia pachyphloia",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 14,
                    "end": 28,
                },
                {
                    "taxon": "Vulpinae",
                    "rank": "section",
                    "trait": "taxon",
                    "start": 30,
                    "end": 38,
                },
            ],
        )

    def test_taxon_11(self):
        self.assertEqual(
            small_test("""Mimosa sensitiva (Bentham) Fox, Trans."""),
            [
                {
                    "authority": "Bentham Fox",
                    "rank": "species",
                    "taxon": "Mimosa sensitiva",
                    "trait": "taxon",
                    "start": 0,
                    "end": 31,
                }
            ],
        )

    def test_taxon_12(self):
        self.assertEqual(
            small_test(
                """
                Neptunia gracilis f. gracilis Neptunia gracilis var. villosula Benth.,
                """
            ),
            [
                {
                    "taxon": "Neptunia gracilis f. gracilis",
                    "rank": "form",
                    "trait": "taxon",
                    "start": 0,
                    "end": 29,
                },
                {
                    "taxon": "Neptunia gracilis var. villosula",
                    "rank": "variety",
                    "authority": "Benth",
                    "trait": "taxon",
                    "start": 30,
                    "end": 69,
                },
            ],
        )

    def test_taxon_13(self):
        """It handles 'F.' genus abbreviation vs 'f.' form abbreviation."""
        self.assertEqual(
            small_test(
                """
                F. gracilis Neptunia gracilis var. villosula Benth.,
                """
            ),
            [
                {
                    "taxon": "F. gracilis",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 11,
                },
                {
                    "taxon": "Neptunia gracilis var. villosula",
                    "rank": "variety",
                    "authority": "Benth",
                    "trait": "taxon",
                    "start": 12,
                    "end": 51,
                },
            ],
        )

    def test_taxon_14(self):
        self.assertEqual(
            small_test("""Ticanto rhombifolia"""),
            [
                {
                    "taxon": "Ticanto rhombifolia",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 19,
                }
            ],
        )

    def test_taxon_15(self):
        """It gets a taxon notation."""
        self.assertEqual(
            small_test(
                """
                Cornaceae
                Cornus obliqua Raf.
                """
            ),
            [
                {
                    "rank": "family",
                    "taxon": "Cornaceae",
                    "trait": "taxon",
                    "start": 0,
                    "end": 9,
                },
                {
                    "authority": "Raf",
                    "rank": "species",
                    "taxon": "Cornus obliqua",
                    "trait": "taxon",
                    "start": 10,
                    "end": 29,
                },
            ],
        )

    def test_taxon_16(self):
        """It gets a family notation."""
        self.assertEqual(
            small_test(
                """
                Crowley's Ridge
                Fabaceae
                Vicia villosa Roth ssp. varia (Khan)
                """
            ),
            [
                {
                    "taxon": "Fabaceae",
                    "rank": "family",
                    "trait": "taxon",
                    "start": 16,
                    "end": 24,
                },
                {
                    "taxon": "Vicia villosa subsp. varia",
                    "rank": "subspecies",
                    "authority": ["Roth", "Khan"],
                    "trait": "taxon",
                    "start": 25,
                    "end": 61,
                },
            ],
        )

    def test_taxon_17(self):
        """It gets the full notation."""
        self.assertEqual(
            small_test("""Cephalanthus occidentalis L. Rubiaceas"""),
            [
                {
                    "taxon": "Cephalanthus occidentalis",
                    "rank": "species",
                    "authority": "L. Rubiaceas",
                    "trait": "taxon",
                    "start": 0,
                    "end": 38,
                }
            ],
        )

    def test_taxon_18(self):
        """It handles 'f.' form abbreviation vs 'F.' genus abbreviation."""
        self.assertEqual(
            small_test("""A. pachyphloia f. brevipinnula."""),
            [
                {
                    "rank": "form",
                    "taxon": "Acacia pachyphloia f. brevipinnula",
                    "trait": "taxon",
                    "start": 0,
                    "end": 30,
                }
            ],
        )

    def test_taxon_19(self):
        """Do not maximize the authority."""
        self.assertEqual(
            small_test(
                """Cornus obliqua Willd.
                In Fraijanes Recreation Park"""
            ),
            [
                {
                    "taxon": "Cornus obliqua",
                    "rank": "species",
                    "authority": "Willd",
                    "trait": "taxon",
                    "start": 0,
                    "end": 21,
                }
            ],
        )

    def test_taxon_20(self):
        """It gets an all caps monomial."""
        self.assertEqual(
            small_test("""PLANTS OF PENNSYLVANIA ASTERACEAE"""),
            [
                {
                    "taxon": "Asteraceae",
                    "rank": "family",
                    "trait": "taxon",
                    "start": 23,
                    "end": 33,
                }
            ],
        )

    def test_taxon_21(self):
        self.assertEqual(
            small_test("""Mimosa sensitiva (L.) Fox, Trans."""),
            [
                {
                    "authority": ["Linnaeus", "Fox"],
                    "rank": "species",
                    "taxon": "Mimosa sensitiva",
                    "trait": "taxon",
                    "start": 0,
                    "end": 26,
                }
            ],
        )

    def test_taxon_22(self):
        self.assertEqual(
            small_test(
                """
                Cephalanthus occidentalis L. Rubiaceas
                Associated species: Cornus obliqua
                """
            ),
            [
                {
                    "taxon": "Cephalanthus occidentalis",
                    "rank": "species",
                    "authority": "L. Rubiaceas",
                    "trait": "taxon",
                    "start": 0,
                    "end": 38,
                },
                {
                    "taxon": "Cornus obliqua",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 59,
                    "end": 73,
                },
            ],
        )

    def test_taxon_23(self):
        self.assertEqual(
            small_test("""Mimosa sensitiva (L.) subsp. varia Fox."""),
            [
                {
                    "authority": ["Linnaeus", "Fox"],
                    "rank": "subspecies",
                    "taxon": "Mimosa sensitiva subsp. varia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 39,
                }
            ],
        )

    def test_taxon_24(self):
        self.assertEqual(
            small_test("""Mimosa sensitiva (R. Person) subsp. varia Fox."""),
            [
                {
                    "authority": ["R. Person", "Fox"],
                    "rank": "subspecies",
                    "taxon": "Mimosa sensitiva subsp. varia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 46,
                }
            ],
        )

    def test_taxon_25(self):
        self.assertEqual(
            small_test("""Mimosa sensitiva (L. Person) subsp. varia Fox."""),
            [
                {
                    "authority": ["L. Person", "Fox"],
                    "rank": "subspecies",
                    "taxon": "Mimosa sensitiva subsp. varia",
                    "trait": "taxon",
                    "start": 0,
                    "end": 46,
                }
            ],
        )

    def test_taxon_26(self):
        """It handles a taxon next to a name with a trailing ID number."""
        self.assertEqual(
            small_test("""Associated species: Neptunia gracilis G. Rink 7075"""),
            [
                {
                    "trait": "taxon",
                    "taxon": "Neptunia gracilis",
                    "rank": "species",
                    "start": 20,
                    "end": 37,
                },
            ],
        )

    def test_taxon_27(self):
        self.assertEqual(
            small_test(""" Name Neptunia gracilis Geyser Locality Vernal, """),
            [
                {
                    "authority": "Geyser",
                    "trait": "taxon",
                    "taxon": "Neptunia gracilis",
                    "rank": "species",
                    "start": 5,
                    "end": 29,
                },
            ],
        )

    def test_taxon_28(self):
        self.assertEqual(
            small_test(""" Neptunia gracilis (Gray) """),
            [
                {
                    "authority": "Gray",
                    "trait": "taxon",
                    "taxon": "Neptunia gracilis",
                    "rank": "species",
                    "start": 0,
                    "end": 24,
                },
            ],
        )

    def test_taxon_29(self):
        self.assertEqual(
            small_test("""Neptunia gracilis & Mimosa sensitiva"""),
            [
                {
                    "rank": "species",
                    "taxon": ["Neptunia gracilis", "Mimosa sensitiva"],
                    "trait": "multi_taxon",
                    "start": 0,
                    "end": 36,
                }
            ],
        )

    def test_taxon_30(self):
        self.assertEqual(
            small_test("""Neptunia gracilis (Roxb.) T. Anderson"""),
            [
                {
                    "authority": "Roxb T. Anderson",
                    "rank": "species",
                    "taxon": "Neptunia gracilis",
                    "trait": "taxon",
                    "start": 0,
                    "end": 37,
                }
            ],
        )

    def test_taxon_31(self):
        self.assertEqual(
            small_test("""Quercus/Cytisus/Agrostis"""),
            [
                {
                    "taxon": "Quercus",
                    "rank": "genus",
                    "trait": "taxon",
                    "start": 0,
                    "end": 7,
                },
                {
                    "taxon": "Cytisus",
                    "rank": "genus",
                    "trait": "taxon",
                    "start": 8,
                    "end": 15,
                },
                {
                    "taxon": "Agrostis",
                    "rank": "genus",
                    "trait": "taxon",
                    "start": 16,
                    "end": 24,
                },
            ],
        )

    def test_taxon_32(self):
        self.assertEqual(
            small_test(
                """Neptunia gracilis Muhl. ex Willd. var. varia (Nutt.) Brewer"""
            ),
            [
                {
                    "taxon": "Neptunia gracilis var. varia",
                    "rank": "variety",
                    "trait": "taxon",
                    "start": 0,
                    "end": 59,
                    "authority": ["Muhl and Willd", "Nutt", "Brewer"],
                }
            ],
        )

    def test_taxon_33(self):
        self.assertEqual(
            small_test("""Neptunia gracilis (L.) Pers."""),
            [
                {
                    "taxon": "Neptunia gracilis",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 28,
                    "authority": ["Linnaeus", "Pers"],
                }
            ],
        )

    def test_taxon_34(self):
        self.assertEqual(
            small_test("""Neptunia gracilis v.Varia by G. McPherson, confirmed Vink"""),
            [
                {
                    "taxon": "Neptunia gracilis var. varia",
                    "rank": "variety",
                    "trait": "taxon",
                    "start": 0,
                    "end": 42,
                    "authority": "G. McPherson",
                },
            ],
        )

    def test_taxon_35(self):
        self.assertEqual(
            small_test(
                "Neptunia gracilis (Torr. & A. Gray ex A. Gray) W.A. Weber & A. Love"
            ),
            [
                {
                    "taxon": "Neptunia gracilis",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 67,
                    "authority": "Torr and A. Gray and A. Gray W. A. Weber and A. Love",
                },
            ],
        )

    def test_taxon_36(self):
        self.assertEqual(
            full_test(
                """
                Neptunia gracilis (Heller) Chuang & Heckard
                ssp. varia (Heller) Chuang & Heckard
                """
            ),
            [
                {
                    "taxon": "Neptunia gracilis subsp. varia",
                    "rank": "subspecies",
                    "trait": "taxon",
                    "start": 0,
                    "end": 80,
                    "authority": [
                        "Heller Chuang and Heckard",
                        "Heller",
                        "Chuang",
                        "Heckard",
                    ],
                }
            ],
        )
