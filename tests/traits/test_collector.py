import unittest

from traiter.pylib.traits.date_ import Date
from traiter.pylib.traits.elevation import Elevation
from traiter.pylib.traits.habitat import Habitat

from flora.pylib.traits.associated_taxon import AssociatedTaxonLabel
from flora.pylib.traits.job import Job
from flora.pylib.traits.taxon import Taxon
from tests.setup import full_test


class TestCollector(unittest.TestCase):
    def test_collector_01(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            full_test("""Sarah Nunn and S. Jacobs and R. Mc Elderry 9480"""),
            [
                Job(
                    trait="job",
                    id_no="9480",
                    name=["Sarah Nunn", "S. Jacobs", "R. Mc Elderry"],
                    job="collector",
                    start=0,
                    end=47,
                )
            ],
        )

    def test_collector_02(self):
        """It does not include the determiner."""
        self.assertEqual(
            full_test(
                """
                Det, Edwin B. Smith
                Coll. Marie P. Locke No. 5595
                """
            ),
            [
                Job(
                    name="Edwin B. Smith",
                    trait="job",
                    job="determiner",
                    start=0,
                    end=19,
                ),
                Job(
                    trait="job",
                    id_no="5595",
                    name="Marie P. Locke",
                    job="collector",
                    start=20,
                    end=49,
                ),
            ],
        )

    def test_collector_03(self):
        """It handles a bad name."""
        self.assertEqual(
            full_test("""Collected by _Wayne.. Hutchins."""),
            [
                Job(
                    trait="job",
                    name="Wayne Hutchins",
                    job="collector",
                    start=0,
                    end=30,
                ),
            ],
        )

    def test_collector_04(self):
        """It parses name suffixes."""
        self.assertEqual(
            full_test("Coll. E. E. Dale, Jr. No. 6061"),
            [
                Job(
                    trait="job",
                    id_no="6061",
                    name="E. E. Dale, Jr.",
                    job="collector",
                    start=0,
                    end=30,
                ),
            ],
        )

    def test_collector_05(self):
        """It parses collectors separated by 'with'."""
        self.assertEqual(
            full_test("Sarah Nunn with Angela Brown 7529 20 October 2002 of"),
            [
                Job(
                    trait="job",
                    id_no="7529",
                    name=["Sarah Nunn", "Angela Brown"],
                    job="collector",
                    start=0,
                    end=33,
                ),
                Date(
                    date="2002-10-20",
                    trait="date",
                    start=34,
                    end=49,
                ),
            ],
        )

    def test_collector_06(self):
        """It parses collectors separated by '&'."""
        self.assertEqual(
            full_test("""Collector: Christopher Reid & Sarah Nunn 2018"""),
            [
                Job(
                    trait="job",
                    id_no="2018",
                    name=["Christopher Reid", "Sarah Nunn"],
                    job="collector",
                    start=0,
                    end=45,
                ),
            ],
        )

    def test_collector_07(self):
        """It handles a number sign."""
        self.assertEqual(
            full_test("""George P. Johnson #5689"""),
            [
                Job(
                    trait="job",
                    id_no="5689",
                    name="George P. Johnson",
                    job="collector",
                    start=0,
                    end=23,
                )
            ],
        )

    def test_collector_08(self):
        """It handles a name with a prefix."""
        self.assertEqual(
            full_test("""Col Mrs. Jim Miller No. 736"""),
            [
                Job(
                    trait="job",
                    id_no="736",
                    name="Mrs. Jim Miller",
                    job="collector",
                    start=0,
                    end=27,
                )
            ],
        )

    def test_collector_09(self):
        self.assertEqual(
            full_test("""collected by Merle Dortmond"""),
            [
                Job(
                    trait="job",
                    name="Merle Dortmond",
                    job="collector",
                    start=0,
                    end=27,
                )
            ],
        )

    def test_collector_10(self):
        self.assertEqual(
            full_test(""" Grassland, GPS 30°"""),
            [Habitat(habitat="grassland", trait="habitat", start=0, end=9)],
        )

    def test_collector_11(self):
        self.assertEqual(
            full_test("""Collector(s): JANET WINGATE No. 4937 Verified: H A Heber"""),
            [
                Job(
                    trait="job",
                    name="JANET WINGATE",
                    id_no="4937",
                    job="collector",
                    start=0,
                    end=36,
                ),
                Job(
                    trait="job",
                    job="verifier",
                    name="H A Heber",
                    start=37,
                    end=56,
                ),
            ],
        )

    def test_collector_12(self):
        self.assertEqual(
            full_test("""3807708N Elev: 1689m."""),
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
            full_test("""TIMON, R16W,"""),
            [],
        )

    def test_collector_14(self):
        self.assertEqual(
            full_test(
                """
                Distribuido List: CRUZ, EBC, MINE
                Collector(s): Timothy J. S. Whitfield
                Collector Number: 1388 Date: 11 Aug 2016"""
            ),
            [
                Job(
                    trait="job",
                    id_no="1388",
                    name="Timothy J. S. Whitfield",
                    job="collector",
                    start=34,
                    end=94,
                ),
                Date(date="2016-08-11", trait="date", start=95, end=112),
            ],
        )

    def test_collector_15(self):
        self.assertEqual(
            full_test(
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
                ),
            ],
        )

    def test_collector_16(self):
        self.assertEqual(
            full_test("""Williams (Rocky) Gleason #F15GLEN55-B"""),
            [
                Job(
                    trait="job",
                    id_no="F15GLEN55-B",
                    name="Williams (Rocky) Gleason",
                    job="collector",
                    start=0,
                    end=37,
                ),
            ],
        )

    def test_collector_17(self):
        self.assertEqual(
            full_test(
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
                ),
            ],
        )

    def test_collector_18(self):
        self.assertEqual(
            full_test("""Frederick H. Utech 91-1178"""),
            [
                Job(
                    trait="job",
                    id_no="91-1178",
                    name="Frederick H. Utech",
                    job="collector",
                    start=0,
                    end=26,
                ),
            ],
        )

    def test_collector_19(self):
        self.assertEqual(
            full_test("""A A.C. Saunders 39141"""),
            [
                Job(
                    trait="job",
                    id_no="39141",
                    name="A A.C. Saunders",
                    job="collector",
                    start=0,
                    end=21,
                ),
            ],
        )

    def test_collector_20(self):
        self.assertEqual(
            full_test("""purple. A A.C. Saunders 39141 14 Apr 2011"""),
            [
                Job(
                    trait="job",
                    id_no="39141",
                    name="A A.C. Saunders",
                    job="collector",
                    start=8,
                    end=29,
                ),
                Date(date="2011-04-14", end=41, start=30, trait="date"),
            ],
        )

    def test_collector_21(self):
        """It handles names with mixed case letters."""
        self.assertEqual(
            full_test("""Wendy McClure 2018-2"""),
            [
                Job(
                    trait="job",
                    id_no="2018-2",
                    name="Wendy McClure",
                    job="collector",
                    start=0,
                    end=20,
                ),
            ],
        )

    def test_collector_22(self):
        """It handles a taxon next to a name."""
        self.assertEqual(
            full_test("""Associated species: Neptunia gracilis G. Rink 7075"""),
            [
                AssociatedTaxonLabel(
                    label="associated species",
                    trait="assoc_taxon_label",
                    start=0,
                    end=18,
                ),
                Taxon(
                    rank="species",
                    trait="taxon",
                    start=20,
                    end=37,
                    taxon="Neptunia gracilis",
                    associated=True,
                ),
                Job(
                    trait="job",
                    name="G. Rink",
                    id_no="7075",
                    job="collector",
                    start=38,
                    end=50,
                ),
            ],
        )

    def test_collector_23(self):
        """It handles a taxon next to a name."""
        self.assertEqual(
            full_test("""collected by Merle Dortmond The University"""),
            [
                Job(
                    trait="job",
                    name="Merle Dortmond",
                    job="collector",
                    start=0,
                    end=27,
                ),
            ],
        )

    def test_collector_24(self):
        """It handles a person after a taxon."""
        self.assertEqual(
            full_test(
                """Associated Species: Cephalanthus occidentalis Cass Blodgett 829"""
            ),
            [
                AssociatedTaxonLabel(
                    label="associated species",
                    trait="assoc_taxon_label",
                    start=0,
                    end=18,
                ),
                Taxon(
                    rank="species",
                    trait="taxon",
                    start=20,
                    end=45,
                    taxon="Cephalanthus occidentalis",
                    associated=True,
                ),
                Job(
                    trait="job",
                    name="Cass Blodgett",
                    id_no="829",
                    job="collector",
                    start=46,
                    end=63,
                ),
            ],
        )

    def test_collector_25(self):
        """It handles a person after a taxon."""
        self.assertEqual(
            full_test("""NCI Code 0GDK0132-Z"""),
            [],
        )

    def test_collector_26(self):
        """It handles a person after a taxon."""
        self.assertEqual(
            full_test(
                """NCI Code 0GDK0132-Z
                Collected by W. Hess, K. Allen, K. Weise, S. Peterson
                """
            ),
            [
                Job(
                    trait="job",
                    name=["W. Hess", "K. Allen", "K. Weise", "S. Peterson"],
                    job="collector",
                    start=20,
                    end=73,
                )
            ],
        )

    def test_collector_27(self):
        """It handles a name separated from their name number."""
        self.maxDiff = None
        self.assertEqual(
            full_test(
                """Little Belt Mountains J.B. Scammons Elevation: 5800 ft.
                No, 105 July 6, 1956"""
            ),
            [
                Job(
                    trait="job",
                    job="collector",
                    start=22,
                    end=35,
                    name="J.B. Scammons",
                    id_no="105",
                ),
                Elevation(
                    elevation=1767.84,
                    units="m",
                    trait="elevation",
                    start=36,
                    end=54,
                ),
                Job(
                    trait="job",
                    name="J.B. Scammons",
                    job="collector",
                    start=56,
                    end=63,
                    id_no="105",
                ),
                Date(date="1956-07-06", trait="date", start=64, end=76),
            ],
        )

    def test_collector_28(self):
        """It handles a name with number and a other collectors."""
        self.assertEqual(
            full_test("""Joshua R. Campbell 327 w/ S. Dickman"""),
            [
                Job(
                    trait="job",
                    name="Joshua R. Campbell",
                    job="collector",
                    start=0,
                    end=22,
                    id_no="327",
                ),
                Job(
                    trait="job",
                    name="S. Dickman",
                    job="other_collector",
                    start=23,
                    end=36,
                ),
            ],
        )

    def test_collector_29(self):
        """It handles a name with number and a other collectors."""
        self.assertEqual(
            full_test("""with Bob Simmons, Dana Griffin & Tom Morris"""),
            [
                Job(
                    trait="job",
                    name=["Bob Simmons", "Dana Griffin", "Tom Morris"],
                    job="other_collector",
                    start=0,
                    end=43,
                ),
            ],
        )

    def test_collector_30(self):
        self.assertEqual(
            full_test("""With: Cindy Smith, Scott Rowan Sponsored by"""),
            [
                Job(
                    trait="job",
                    name=["Cindy Smith", "Scott Rowan"],
                    job="other_collector",
                    start=0,
                    end=30,
                ),
            ],
        )

    def test_collector_31(self):
        self.assertEqual(
            full_test("""Joni Ward 866-a"""),
            [
                Job(
                    trait="job",
                    name="Joni Ward",
                    job="collector",
                    id_no="866-a",
                    start=0,
                    end=15,
                ),
            ],
        )

    def test_collector_32(self):
        self.assertEqual(
            full_test("""Cole Larsson-Whittaker 866-a"""),
            [
                Job(
                    trait="job",
                    name="Cole Larsson-Whittaker",
                    job="collector",
                    id_no="866-a",
                    start=0,
                    end=28,
                ),
            ],
        )

    def test_collector_33(self):
        self.assertEqual(
            full_test("""Collectors: Avena Nelson, Elias Nelson."""),
            [
                Job(
                    trait="job",
                    name=["Avena Nelson", "Elias Nelson"],
                    job="collector",
                    start=0,
                    end=38,
                ),
            ],
        )

    def test_collector_34(self):
        self.assertEqual(
            full_test("""of Ua C. Riverside (UCR)y Canis"""),
            [],
        )

    def test_collector_35(self):
        self.assertEqual(
            full_test(
                """Voucher Project Cactaceae Carnegiea gigantea
                accession number 0075
                """
            ),
            [],
        )

    def test_collector_36(self):
        self.assertEqual(
            full_test("""Mimosa sensitiva Collected by: E. Mohr"""),
            [
                Taxon(
                    taxon="Mimosa sensitiva",
                    rank="species",
                    trait="taxon",
                    start=0,
                    end=16,
                ),
                Job(trait="job", name="E. Mohr", job="collector", start=17, end=38),
            ],
        )

    def test_collector_37(self):
        self.assertEqual(
            full_test(
                """
                with Juan Kaplan, Helena Walker Herbarium of a Botanical Garden"""
            ),
            [
                Job(
                    trait="job",
                    name=["Juan Kaplan", "Helena Walker"],
                    job="other_collector",
                    start=0,
                    end=31,
                )
            ],
        )

    def test_collector_38(self):
        self.maxDiff = None
        self.assertEqual(
            full_test("""4 September 2008 J. Johnson with M. King Herbarium"""),
            [
                Date(
                    date="2008-09-04",
                    trait="date",
                    start=0,
                    end=16,
                ),
                Job(
                    trait="job",
                    name="J. Johnson",
                    job="collector",
                    start=17,
                    end=27,
                ),
                Job(
                    trait="job",
                    name="M. King",
                    job="other_collector",
                    start=28,
                    end=40,
                ),
            ],
        )

    def test_collector_39(self):
        self.assertEqual(
            full_test(
                """
                HR1998-01
                H. Richey
                """
            ),
            [
                Job(
                    trait="job",
                    name="H. Richey",
                    job="collector",
                    id_no="HR1998-01",
                    start=0,
                    end=19,
                ),
            ],
        )

    def test_collector_40(self):
        self.assertEqual(
            full_test("""AC Saunders 34380 OS"""),
            [
                Job(
                    trait="job",
                    name="AC Saunders",
                    job="collector",
                    id_no="34380",
                    start=0,
                    end=17,
                ),
            ],
        )

    def test_collector_41(self):
        self.assertEqual(
            full_test(
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
                    start=9,
                    end=42,
                ),
            ],
        )

    def test_collector_42(self):
        self.assertEqual(
            full_test(
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
                    start=0,
                    end=51,
                )
            ],
        )

    def test_collector_43(self):
        self.assertEqual(
            full_test("""w/ Mark A. Elvin, Tim Thomas"""),
            [
                Job(
                    trait="job",
                    name=["Mark A. Elvin", "Tim Thomas"],
                    job="other_collector",
                    start=0,
                    end=28,
                )
            ],
        )
