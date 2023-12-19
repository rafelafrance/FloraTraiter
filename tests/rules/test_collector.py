import unittest

from flora.pylib.rules.associated_taxon_label import AssociatedTaxonLabel
from flora.pylib.rules.id_number import IdNumber
from flora.pylib.rules.job import Job
from flora.pylib.rules.taxon import Taxon
from tests.setup import parse
from traiter.traiter.pylib.rules.date_ import Date
from traiter.traiter.pylib.rules.elevation import Elevation
from traiter.traiter.pylib.rules.habitat import Habitat


class TestCollector(unittest.TestCase):
    def test_collector_01(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            parse("""Sarah Nunn and S. Jacobs and R. Mc Elderry 9480"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=42,
                    job="collector",
                    name=["Sarah Nunn", "S. Jacobs", "R. Mc Elderry"],
                ),
                IdNumber(
                    trait="id_number",
                    start=43,
                    end=47,
                    number="9480",
                    type="record_number",
                ),
            ],
        )

    def test_collector_02(self):
        """It does not include the determiner."""
        self.assertEqual(
            parse(
                """
                Det, Edwin B. Smith
                Coll. Marie P. Locke No. 5595
                """
            ),
            [
                Job(
                    trait="job",
                    start=0,
                    end=19,
                    job="determiner",
                    name="Edwin B. Smith",
                    has_label=True,
                ),
                Job(
                    trait="job",
                    start=20,
                    end=40,
                    job="collector",
                    name="Marie P. Locke",
                    has_label=True,
                ),
                IdNumber(
                    trait="id_number",
                    start=41,
                    end=49,
                    number="5595",
                    type="record_number",
                    has_label=True,
                ),
            ],
        )

    def test_collector_03(self):
        """It handles a bad name."""
        self.assertEqual(
            parse("""Collected by _Wayne.. Hutchins."""),
            [
                Job(
                    trait="job",
                    name="Wayne Hutchins",
                    job="collector",
                    start=0,
                    end=30,
                    has_label=True,
                ),
            ],
        )

    def test_collector_04(self):
        """It parses name suffixes."""
        self.assertEqual(
            parse("Coll. E. E. Dale, Jr. No. 6061"),
            [
                Job(
                    trait="job",
                    start=0,
                    end=21,
                    job="collector",
                    name="E. E. Dale, Jr.",
                    has_label=True,
                ),
                IdNumber(
                    trait="id_number",
                    start=22,
                    end=30,
                    number="6061",
                    type="record_number",
                    has_label=True,
                ),
            ],
        )

    def test_collector_05(self):
        """It parses collectors separated by 'with'."""
        self.maxDiff = None
        self.assertEqual(
            parse("Sarah Nunn with Angela Brown 7529 20 October 2002 of"),
            [
                Job(
                    trait="job",
                    start=0,
                    end=28,
                    job="collector",
                    name=["Sarah Nunn", "Angela Brown"],
                ),
                IdNumber(
                    trait="id_number",
                    start=29,
                    end=33,
                    number="7529",
                    type="record_number",
                ),
                Date(trait="date", start=34, end=49, date="2002-10-20"),
            ],
        )

    def test_collector_06(self):
        """It parses collectors separated by '&'."""
        self.assertEqual(
            parse("""Collector: Christopher Reid & Sarah Nunn 2018"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=40,
                    job="collector",
                    name=["Christopher Reid", "Sarah Nunn"],
                    has_label=True,
                ),
                IdNumber(
                    trait="id_number",
                    start=41,
                    end=45,
                    number="2018",
                    type="record_number",
                ),
            ],
        )

    def test_collector_07(self):
        """It handles a number sign."""
        self.assertEqual(
            parse("""George P. Johnson #5689"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=17,
                    job="collector",
                    name="George P. Johnson",
                ),
                IdNumber(
                    trait="id_number",
                    start=18,
                    end=23,
                    number="5689",
                    type="record_number",
                    has_label=True,
                ),
            ],
        )

    def test_collector_08(self):
        """It handles a name with a prefix."""
        self.assertEqual(
            parse("""Col Mrs. Jim Miller No. 736"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=19,
                    job="collector",
                    name="Mrs. Jim Miller",
                    has_label=True,
                ),
                IdNumber(
                    trait="id_number",
                    start=20,
                    end=27,
                    number="736",
                    type="record_number",
                    has_label=True,
                ),
            ],
        )

    def test_collector_09(self):
        self.assertEqual(
            parse("""collected by Merle Dortmond"""),
            [
                Job(
                    trait="job",
                    name="Merle Dortmond",
                    job="collector",
                    start=0,
                    end=27,
                    has_label=True,
                )
            ],
        )

    def test_collector_10(self):
        self.assertEqual(
            parse(""" Grassland, GPS 30°"""),
            [Habitat(habitat="grassland", trait="habitat", start=0, end=9)],
        )

    def test_collector_11(self):
        self.assertEqual(
            parse("""Collector(s): JANET WINGATE No. 4937 Verified: H A Heber"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=27,
                    job="collector",
                    name="JANET WINGATE",
                    has_label=True,
                ),
                IdNumber(
                    trait="id_number",
                    start=28,
                    end=36,
                    number="4937",
                    type="record_number",
                    has_label=True,
                ),
                Job(
                    trait="job",
                    start=37,
                    end=56,
                    has_label=True,
                    job="verifier",
                    name="H A Heber",
                ),
            ],
        )

    def test_collector_12(self):
        self.assertEqual(
            parse("""3807708N Elev: 1689m."""),
            [
                Elevation(
                    elevation=1689.0,
                    units="m",
                    trait="elevation",
                    start=9,
                    end=21,
                )
            ],
        )

    def test_collector_13(self):
        self.assertEqual(
            parse("""TIMON, R16W,"""),
            [],
        )

    def test_collector_14(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                """
                Distribuido List: CRUZ, EBC, MINE
                Collector(s): Timothy J. S. Whitfield
                Collector Number: 1388 Date: 11 Aug 2016"""
            ),
            [
                Job(
                    trait="job",
                    start=34,
                    end=71,
                    job="collector",
                    name="Timothy J. S. Whitfield",
                    has_label=True,
                ),
                IdNumber(
                    trait="id_number",
                    start=72,
                    end=94,
                    number="1388",
                    type="collector_id",
                    has_label=True,
                ),
                Date(trait="date", start=95, end=112, date="2016-08-11"),
            ],
        )

    def test_collector_15(self):
        self.assertEqual(
            parse(
                """
                With: Dawn Goldman, Army Prince, Steven Emrick, Janet Smith,
                Diane Hicks, Beechnut
                """
            ),
            [
                Job(
                    trait="job",
                    name=[
                        "Dawn Goldman",
                        "Army Prince",
                        "Steven Emrick",
                        "Janet Smith",
                        "Diane Hicks",
                        "Beechnut",
                    ],
                    job="other_collector",
                    start=0,
                    end=82,
                    has_label=True,
                ),
            ],
        )

    def test_collector_16(self):
        self.assertEqual(
            parse("""Williams (Rocky) Gleason #F15GLEN55-B"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=24,
                    job="collector",
                    name="Williams (Rocky) Gleason",
                ),
                IdNumber(
                    trait="id_number",
                    start=25,
                    end=37,
                    number="F15GLEN55-B",
                    type="record_number",
                    has_label=True,
                ),
            ],
        )

    def test_collector_17(self):
        self.assertEqual(
            parse(
                """
                With: Dixie Damrel, Sarah Hunkins, Steven and Johan LaMoure
                """
            ),
            [
                Job(
                    trait="job",
                    name=[
                        "Dixie Damrel",
                        "Sarah Hunkins",
                        "Steven and Johan LaMoure",
                    ],
                    job="other_collector",
                    start=0,
                    end=59,
                    has_label=True,
                ),
            ],
        )

    def test_collector_18(self):
        self.assertEqual(
            parse("""Frederick H. Utech 91-1178"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=18,
                    job="collector",
                    name="Frederick H. Utech",
                ),
                IdNumber(
                    trait="id_number",
                    start=19,
                    end=26,
                    number="91-1178",
                    type="record_number",
                ),
            ],
        )

    def test_collector_19(self):
        self.assertEqual(
            parse("""A A.C. Saunders 39141"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=15,
                    job="collector",
                    name="A A.C. Saunders",
                ),
                IdNumber(
                    trait="id_number",
                    start=16,
                    end=21,
                    number="39141",
                    type="record_number",
                ),
            ],
        )

    def test_collector_20(self):
        self.assertEqual(
            parse("""purple. A A.C. Saunders 39141 14 Apr 2011"""),
            [
                Job(
                    trait="job",
                    start=8,
                    end=23,
                    job="collector",
                    name="A A.C. Saunders",
                ),
                IdNumber(
                    trait="id_number",
                    start=24,
                    end=29,
                    number="39141",
                    type="record_number",
                ),
                Date(trait="date", start=30, end=41, date="2011-04-14"),
            ],
        )

    def test_collector_21(self):
        """It handles names with mixed case letters."""
        self.assertEqual(
            parse("""Wendy McClure 2018-2"""),
            [
                Job(
                    trait="job", start=0, end=13, job="collector", name="Wendy McClure"
                ),
                IdNumber(
                    trait="id_number",
                    start=14,
                    end=20,
                    number="2018-2",
                    type="record_number",
                ),
            ],
        )

    def test_collector_22(self):
        """It handles a taxon next to a name."""
        self.assertEqual(
            parse("""Associated species: Neptunia gracilis G. Rink 7075"""),
            [
                AssociatedTaxonLabel(
                    trait="assoc_taxon_label",
                    start=0,
                    end=18,
                    label="associated species",
                ),
                Taxon(
                    trait="taxon",
                    start=20,
                    end=37,
                    taxon="Neptunia gracilis",
                    rank="species",
                    associated=True,
                ),
                Job(trait="job", start=38, end=45, job="collector", name="G. Rink"),
                IdNumber(
                    trait="id_number",
                    start=46,
                    end=50,
                    number="7075",
                    type="record_number",
                ),
            ],
        )

    def test_collector_23(self):
        """It handles a taxon next to a name."""
        self.assertEqual(
            parse("""collected by Merle Dortmond The University"""),
            [
                Job(
                    trait="job",
                    name="Merle Dortmond",
                    job="collector",
                    has_label=True,
                    start=0,
                    end=27,
                ),
            ],
        )

    def test_collector_24(self):
        """It handles a person after a taxon."""
        self.assertEqual(
            parse(
                """Associated Species: Cephalanthus occidentalis Cass Blodgett 829"""
            ),
            [
                AssociatedTaxonLabel(
                    trait="assoc_taxon_label",
                    start=0,
                    end=18,
                    label="associated species",
                ),
                Taxon(
                    trait="taxon",
                    start=20,
                    end=45,
                    taxon="Cephalanthus occidentalis",
                    rank="species",
                    associated=True,
                ),
                Job(
                    trait="job", start=46, end=59, job="collector", name="Cass Blodgett"
                ),
                IdNumber(
                    trait="id_number",
                    start=60,
                    end=63,
                    number="829",
                    type="record_number",
                ),
            ],
        )

    def test_collector_25(self):
        self.assertEqual(
            parse("""NCI Code 0GDK0132-Z"""),
            [],
        )

    def test_collector_26(self):
        self.assertEqual(
            parse(
                """NCI Code 0GDK0132-Z
                Collected by W. Hess, K. Allen, K. Weise, S. Peterson
                """
            ),
            [
                Job(
                    trait="job",
                    name=["W. Hess", "K. Allen", "K. Weise", "S. Peterson"],
                    job="collector",
                    has_label=True,
                    start=20,
                    end=73,
                )
            ],
        )

    def test_collector_27(self):
        """It handles a name separated from their name number."""
        self.assertEqual(
            parse(
                """Little Belt Mountains J.B. Scammons Elevation: 5800 ft.
                No, 105 July 6, 1956"""
            ),
            [
                Job(
                    trait="job", start=22, end=35, job="collector", name="J.B. Scammons"
                ),
                Elevation(
                    trait="elevation", start=36, end=54, elevation=1767.84, units="m"
                ),
                IdNumber(
                    trait="id_number",
                    start=56,
                    end=63,
                    number=",105",
                    type="record_number",
                    has_label=True,
                ),
                Date(trait="date", start=64, end=76, date="1956-07-06"),
            ],
        )

    def test_collector_28(self):
        """It handles a name with number and other collectors."""
        self.assertEqual(
            parse("""Joshua R. Campbell 327 w/ S. Dickman"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=18,
                    job="collector",
                    name="Joshua R. Campbell",
                ),
                IdNumber(
                    trait="id_number",
                    start=19,
                    end=22,
                    number="327",
                    type="record_number",
                ),
                Job(
                    trait="job",
                    start=23,
                    end=36,
                    job="other_collector",
                    name="S. Dickman",
                    has_label=True,
                ),
            ],
        )

    def test_collector_29(self):
        """It handles a name with number and a other collectors."""
        self.assertEqual(
            parse("""with Bob Simmons, Dana Griffin & Tom Morris"""),
            [
                Job(
                    trait="job",
                    name=["Bob Simmons", "Dana Griffin", "Tom Morris"],
                    job="other_collector",
                    has_label=True,
                    start=0,
                    end=43,
                ),
            ],
        )

    def test_collector_30(self):
        self.assertEqual(
            parse("""With: Cindy Smith, Scott Rowan Sponsored by"""),
            [
                Job(
                    trait="job",
                    name=["Cindy Smith", "Scott Rowan"],
                    job="other_collector",
                    has_label=True,
                    start=0,
                    end=30,
                ),
            ],
        )

    def test_collector_31(self):
        self.assertEqual(
            parse("""Joni Ward 866-a"""),
            [
                Job(trait="job", start=0, end=9, job="collector", name="Joni Ward"),
                IdNumber(
                    trait="id_number",
                    start=10,
                    end=15,
                    number="866-a",
                    type="record_number",
                ),
            ],
        )

    def test_collector_32(self):
        self.assertEqual(
            parse("""Cole Larsson-Whittaker 866-a"""),
            [
                Job(
                    trait="job",
                    start=0,
                    end=22,
                    job="collector",
                    name="Cole Larsson-Whittaker",
                ),
                IdNumber(
                    trait="id_number",
                    start=23,
                    end=28,
                    number="866-a",
                    type="record_number",
                ),
            ],
        )

    def test_collector_33(self):
        self.assertEqual(
            parse("""Collectors: Avena Nelson, Elias Nelson."""),
            [
                Job(
                    trait="job",
                    name=["Avena Nelson", "Elias Nelson"],
                    job="collector",
                    has_label=True,
                    start=0,
                    end=38,
                ),
            ],
        )

    def test_collector_34(self):
        self.assertEqual(
            parse("""of Ua C. Riverside (UCR)y Canis"""),
            [],
        )

    def test_collector_35(self):
        self.assertEqual(
            parse(
                """Voucher Project Cactaceae Carnegiea gigantea
                accession number 0075
                """
            ),
            [
                IdNumber(
                    trait="id_number",
                    start=45,
                    end=66,
                    number="0075",
                    type="accession_number",
                    has_label=True,
                )
            ],
        )

    def test_collector_36(self):
        self.assertEqual(
            parse("""Mimosa sensitiva Collected by: E. Mohr"""),
            [
                Taxon(
                    taxon="Mimosa sensitiva",
                    rank="species",
                    trait="taxon",
                    start=0,
                    end=16,
                ),
                Job(
                    trait="job",
                    name="E. Mohr",
                    job="collector",
                    has_label=True,
                    start=17,
                    end=38,
                ),
            ],
        )

    def test_collector_37(self):
        self.assertEqual(
            parse(
                """
                with Juan Kaplan, Helena Walker Herbarium of a Botanical Garden"""
            ),
            [
                Job(
                    trait="job",
                    name=["Juan Kaplan", "Helena Walker"],
                    job="other_collector",
                    has_label=True,
                    start=0,
                    end=31,
                )
            ],
        )

    def test_collector_38(self):
        self.assertEqual(
            parse("""4 September 2008 J. Johnson with M. King Herbarium"""),
            [
                Date(trait="date", start=0, end=16, date="2008-09-04"),
                Job(
                    trait="job",
                    start=17,
                    end=40,
                    job="collector",
                    name=["J. Johnson", "M. King"],
                ),
            ],
        )

    def test_collector_39(self):
        self.assertEqual(
            parse(
                """
                HR1998-01
                H. Richey
                """
            ),
            [
                IdNumber(
                    trait="id_number",
                    start=0,
                    end=9,
                    number="HR1998-01",
                    type="record_number",
                ),
                Job(trait="job", start=10, end=19, job="collector", name="H. Richey"),
            ],
        )

    def test_collector_40(self):
        self.assertEqual(
            parse("""AC Saunders 34380 OS"""),
            [
                Job(trait="job", start=0, end=11, job="collector", name="AC Saunders"),
                IdNumber(
                    trait="id_number",
                    start=12,
                    end=17,
                    number="34380",
                    type="record_number",
                ),
            ],
        )

    def test_collector_41(self):
        self.assertEqual(
            parse(
                """
                Roadside
                COLLECTOR Lytle McGill, Roy Brown ELEV
                """
            ),
            [
                Job(
                    trait="job",
                    name=["Lytle McGill", "Roy Brown"],
                    job="collector",
                    has_label=True,
                    start=9,
                    end=42,
                ),
            ],
        )

    def test_collector_42(self):
        self.assertEqual(
            parse(
                """
                With: Marcelline VandeWater, Steven Williams, Janet
                Rosenthal
                """
            ),
            [
                Job(
                    trait="job",
                    name=[
                        "Marcelline VandeWater",
                        "Steven Williams",
                        "Janet",
                    ],
                    job="other_collector",
                    has_label=True,
                    start=0,
                    end=51,
                )
            ],
        )

    def test_collector_43(self):
        self.assertEqual(
            parse("""w/ Mark A. Elvin, Tim Thomas"""),
            [
                Job(
                    trait="job",
                    name=["Mark A. Elvin", "Tim Thomas"],
                    job="other_collector",
                    has_label=True,
                    start=0,
                    end=28,
                )
            ],
        )
