import unittest

from flora.pylib.rules.admin_unit import AdminUnit
from flora.pylib.rules.associated_taxon_label import AssociatedTaxonLabel
from flora.pylib.rules.id_number import IdNumber
from flora.pylib.rules.job import Job
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
                    trait="taxon",
                    start=0,
                    end=12,
                )
            ],
        )

    def test_taxon_02(self):
        self.assertEqual(
            parse("""Mimosa sensitiva"""),
            [
                Taxon(
                    rank="species",
                    taxon="Mimosa sensitiva",
                    trait="taxon",
                    start=0,
                    end=16,
                )
            ],
        )

    def test_taxon_03(self):
        self.assertEqual(
            parse("""M. polycarpa var. spegazzinii"""),
            [
                Taxon(
                    rank="variety",
                    taxon="M. polycarpa var. spegazzinii",
                    trait="taxon",
                    start=0,
                    end=29,
                )
            ],
        )

    def test_taxon_04(self):
        self.assertEqual(
            parse("""A. pachyphloia subsp. brevipinnula."""),
            [
                Taxon(
                    rank="subspecies",
                    taxon="Acacia pachyphloia subsp. brevipinnula",
                    trait="taxon",
                    start=0,
                    end=34,
                )
            ],
        )

    def test_taxon_05(self):
        self.assertEqual(
            parse("""A. pachyphloia Bamehy 184."""),
            [
                Taxon(
                    rank="species",
                    taxon="Acacia pachyphloia",
                    trait="taxon",
                    authority="Bamehy",
                    start=0,
                    end=21,
                )
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
                    trait="taxon",
                    start=0,
                    end=29,
                )
            ],
        )

    def test_taxon_07(self):
        self.assertEqual(
            parse("""Ser. Vulpinae is characterized"""),
            [
                Taxon(
                    rank="series",
                    taxon="Vulpinae",
                    trait="taxon",
                    start=0,
                    end=13,
                    associated=True,
                )
            ],
        )

    def test_taxon_08(self):
        self.assertEqual(
            parse("""All species are trees"""),
            [Part(end=21, part="tree", start=16, trait="part", type="plant_part")],
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
                    trait="taxon",
                    start=14,
                    end=28,
                ),
                Taxon(
                    taxon="Vulpinae",
                    rank="section",
                    trait="taxon",
                    start=30,
                    end=38,
                    associated=True,
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
                    trait="taxon",
                    start=0,
                    end=31,
                )
            ],
        )

    def test_taxon_12(self):
        self.assertEqual(
            parse(
                """
                Neptunia gracilis f. gracilis Neptunia gracilis var. villosula Benth.,
                """
            ),
            [
                Taxon(
                    taxon="Neptunia gracilis f. gracilis",
                    rank="form",
                    trait="taxon",
                    start=0,
                    end=29,
                ),
                Taxon(
                    taxon="Neptunia gracilis var. villosula",
                    rank="variety",
                    authority="Benth",
                    trait="taxon",
                    start=30,
                    end=69,
                    associated=True,
                ),
            ],
        )

    def test_taxon_13(self):
        """It handles 'F.' genus abbreviation vs 'f.' form abbreviation."""
        self.assertEqual(
            parse(
                """
                F. gracilis Neptunia gracilis var. villosula Benth.,
                """
            ),
            [
                Taxon(
                    taxon="F. gracilis",
                    rank="species",
                    trait="taxon",
                    start=0,
                    end=11,
                ),
                Taxon(
                    taxon="Neptunia gracilis var. villosula",
                    rank="variety",
                    authority="Benth",
                    trait="taxon",
                    start=12,
                    end=51,
                    associated=True,
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
                    trait="taxon",
                    start=0,
                    end=19,
                )
            ],
        )

    def test_taxon_15(self):
        """It gets a taxon notation."""
        self.assertEqual(
            parse(
                """
                Cornaceae
                Cornus obliqua Raf.
                """
            ),
            [
                Taxon(
                    rank="family",
                    taxon="Cornaceae",
                    trait="taxon",
                    start=0,
                    end=9,
                    associated=True,
                ),
                Taxon(
                    authority="Raf",
                    rank="species",
                    taxon="Cornus obliqua",
                    trait="taxon",
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
                """
            ),
            [
                Taxon(
                    taxon="Fabaceae",
                    rank="family",
                    trait="taxon",
                    start=16,
                    end=24,
                    associated=True,
                ),
                Taxon(
                    taxon="Vicia villosa subsp. varia",
                    rank="subspecies",
                    authority=["Roth", "Khan"],
                    trait="taxon",
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
                    trait="taxon",
                    start=0,
                    end=38,
                )
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
                    trait="taxon",
                    start=0,
                    end=30,
                )
            ],
        )

    def test_taxon_19(self):
        """Do not maximize the authority."""
        self.assertEqual(
            parse(
                """Cornus obliqua Willd.
                In Fraijanes Recreation Park"""
            ),
            [
                Taxon(
                    taxon="Cornus obliqua",
                    rank="species",
                    authority="Willd",
                    trait="taxon",
                    start=0,
                    end=21,
                )
            ],
        )

    def test_taxon_20(self):
        """It gets an all caps monomial."""
        self.assertEqual(
            parse("""PLANTS OF PENNSYLVANIA ASTERACEAE"""),
            [
                AdminUnit(trait="admin_unit", start=0, end=22, us_state="Pennsylvania"),
                Taxon(
                    taxon="Asteraceae",
                    rank="family",
                    trait="taxon",
                    start=23,
                    end=33,
                    associated=True,
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
                    trait="taxon",
                    start=0,
                    end=26,
                )
            ],
        )

    def test_taxon_22(self):
        self.assertEqual(
            parse(
                """
                Cephalanthus occidentalis L. Rubiaceas
                Associated species: Cornus obliqua
                """
            ),
            [
                Taxon(
                    taxon="Cephalanthus occidentalis",
                    rank="species",
                    authority="L. Rubiaceas",
                    trait="taxon",
                    start=0,
                    end=38,
                ),
                AssociatedTaxonLabel(
                    trait="assoc_taxon_label",
                    label="associated species",
                    start=39,
                    end=57,
                ),
                Taxon(
                    taxon="Cornus obliqua",
                    rank="species",
                    trait="taxon",
                    start=59,
                    end=73,
                    associated=True,
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
                    trait="taxon",
                    start=0,
                    end=39,
                )
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
                    trait="taxon",
                    start=0,
                    end=46,
                )
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
                    trait="taxon",
                    start=0,
                    end=46,
                )
            ],
        )

    def test_taxon_26(self):
        """It handles a taxon next to a name with a trailing ID number."""
        self.maxDiff = None
        self.assertEqual(
            parse("""Associated species: Neptunia gracilis G. Rink 7075"""),
            [
                AssociatedTaxonLabel(
                    trait="assoc_taxon_label",
                    start=0,
                    end=18,
                    _text="Associated species",
                    label="associated species",
                ),
                Taxon(
                    trait="taxon",
                    start=20,
                    end=37,
                    _text="Neptunia gracilis",
                    taxon="Neptunia gracilis",
                    rank="species",
                    associated=True,
                ),
                Job(
                    trait="job",
                    start=38,
                    end=45,
                    _text="G. Rink",
                    job="collector",
                    name="G. Rink",
                ),
                IdNumber(
                    trait="id_number",
                    start=46,
                    end=50,
                    _text="7075",
                    number="7075",
                    type="record_number",
                ),
            ],
        )

    def test_taxon_27(self):
        self.assertEqual(
            parse(""" Name Neptunia gracilis Geyser Locality Vernal, """),
            [
                Taxon(
                    authority="Geyser",
                    trait="taxon",
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
                    trait="taxon",
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
                    trait="multi_taxon",
                    start=0,
                    end=36,
                )
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
                    trait="taxon",
                    start=0,
                    end=37,
                )
            ],
        )

    def test_taxon_31(self):
        self.assertEqual(
            parse("""Quercus/Cytisus/Agrostis"""),
            [
                Taxon(
                    taxon="Quercus",
                    rank="genus",
                    trait="taxon",
                    start=0,
                    end=7,
                    associated=True,
                ),
                Taxon(
                    taxon="Cytisus",
                    rank="genus",
                    trait="taxon",
                    start=8,
                    end=15,
                    associated=True,
                ),
                Taxon(
                    taxon="Agrostis",
                    rank="genus",
                    trait="taxon",
                    start=16,
                    end=24,
                    associated=True,
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
                    trait="taxon",
                    start=0,
                    end=59,
                    authority=["Muhl and Willd", "Nutt", "Brewer"],
                )
            ],
        )

    def test_taxon_33(self):
        self.assertEqual(
            parse("""Neptunia gracilis (L.) Pers."""),
            [
                Taxon(
                    taxon="Neptunia gracilis",
                    rank="species",
                    trait="taxon",
                    start=0,
                    end=28,
                    authority="Linnaeus, Pers",
                )
            ],
        )

    def test_taxon_34(self):
        self.assertEqual(
            parse("""Neptunia gracilis v.Varia by G. McPherson, confirmed Vink"""),
            [
                Taxon(
                    taxon="Neptunia gracilis var. varia",
                    rank="variety",
                    trait="taxon",
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
                "Neptunia gracilis (Torr. & A. Gray ex A. Gray) W.A. Weber & A. Love"
            ),
            [
                Taxon(
                    taxon="Neptunia gracilis",
                    rank="species",
                    trait="taxon",
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
                """
            ),
            [
                Taxon(
                    taxon="Neptunia gracilis subsp. varia",
                    rank="subspecies",
                    trait="taxon",
                    start=0,
                    end=80,
                    authority=[
                        "Heller Chuang and Heckard",
                        "Heller",
                        "Chuang",
                        "Heckard",
                    ],
                )
            ],
        )

    def test_taxon_37(self):
        self.assertEqual(
            parse("""Neptunia gracilis var. varia (A. Gray) N.H. Holmgren,"""),
            [
                Taxon(
                    taxon="Neptunia gracilis var. varia",
                    rank="variety",
                    trait="taxon",
                    start=0,
                    end=53,
                    authority="A. Gray N.H. Holmgren",
                )
            ],
        )
