import unittest

from tests.setup import full_test


class TestCollector(unittest.TestCase):
    def test_collector_01(self):
        """It gets a multiple name notations."""
        self.assertEqual(
            full_test("""Sarah Nunn and S. Jacobs and R. Mc Elderry 9480"""),
            [
                {
                    "collector_no": "9480",
                    "collector": ["Sarah Nunn", "S. Jacobs", "R. Mc Elderry"],
                    "trait": "collector",
                    "start": 0,
                    "end": 47,
                }
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
                {
                    "determiner": "Edwin B. Smith",
                    "trait": "determiner",
                    "start": 0,
                    "end": 19,
                },
                {
                    "collector_no": "5595",
                    "collector": "Marie P. Locke",
                    "trait": "collector",
                    "start": 20,
                    "end": 49,
                },
            ],
        )

    def test_collector_03(self):
        """It handles a bad name."""
        self.assertEqual(
            full_test("""Collected by _Wayne.. Hutchins."""),
            [
                {
                    "collector": "Wayne Hutchins",
                    "trait": "collector",
                    "start": 0,
                    "end": 30,
                },
            ],
        )

    def test_collector_04(self):
        """It handles random words matching names."""
        self.assertEqual(
            full_test("""Collected by _Wayne.. Hutchins."""),
            [
                {
                    "collector": "Wayne Hutchins",
                    "trait": "collector",
                    "start": 0,
                    "end": 30,
                },
            ],
        )

    def test_collector_05(self):
        """It parses name suffixes."""
        self.assertEqual(
            full_test("Coll. E. E. Dale, Jr. No. 6061"),
            [
                {
                    "collector_no": "6061",
                    "collector": "E. E. Dale, Jr.",
                    "trait": "collector",
                    "start": 0,
                    "end": 30,
                },
            ],
        )

    def test_collector_06(self):
        """It parses collectors separated by 'with'."""
        self.assertEqual(
            full_test("Sarah Nunn with Angela Brown 7529 20 October 2002 of"),
            [
                {
                    "collector_no": "7529",
                    "collector": ["Sarah Nunn", "Angela Brown"],
                    "trait": "collector",
                    "start": 0,
                    "end": 33,
                },
                {
                    "date": "2002-10-20",
                    "trait": "date",
                    "start": 34,
                    "end": 49,
                },
            ],
        )

    def test_collector_07(self):
        """It parses collectors separated by '&'."""
        self.assertEqual(
            full_test("""Collector: Christopher Reid & Sarah Nunn 2018"""),
            [
                {
                    "collector_no": "2018",
                    "collector": ["Christopher Reid", "Sarah Nunn"],
                    "trait": "collector",
                    "start": 0,
                    "end": 45,
                },
            ],
        )

    def test_collector_08(self):
        """It handles a number sign."""
        self.assertEqual(
            full_test("""George P. Johnson #5689"""),
            [
                {
                    "collector_no": "5689",
                    "collector": "George P. Johnson",
                    "trait": "collector",
                    "start": 0,
                    "end": 23,
                }
            ],
        )

    def test_collector_09(self):
        """It handles a name with a prefix."""
        self.assertEqual(
            full_test("""Col Mrs. Jim Miller No. 736"""),
            [
                {
                    "collector_no": "736",
                    "collector": "Mrs. Jim Miller",
                    "trait": "collector",
                    "start": 0,
                    "end": 27,
                }
            ],
        )

    def test_collector_10(self):
        self.assertEqual(
            full_test("""collected by Merle Dortmond"""),
            [
                {
                    "collector": "Merle Dortmond",
                    "trait": "collector",
                    "start": 0,
                    "end": 27,
                }
            ],
        )

    def test_collector_11(self):
        self.assertEqual(
            full_test(""" Grassland, GPS 30°"""),
            [{"habitat": "grassland", "trait": "habitat", "start": 0, "end": 9}],
        )

    def test_collector_12(self):
        self.assertEqual(
            full_test("""3807708N Elev: 1689m."""),
            [
                {
                    "elevation": 1689.0,
                    "units": "m",
                    "trait": "elevation",
                    "start": 9,
                    "end": 21,
                }
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
                {
                    "collector_no": "1388",
                    "collector": "Timothy J. S. Whitfield",
                    "trait": "collector",
                    "start": 34,
                    "end": 94,
                },
                {"date": "2016-08-11", "trait": "date", "start": 95, "end": 112},
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
                {
                    "other_collector": [
                        "Dawn Goldman",
                        "Army Prince",
                        "Steven Emrick",
                        "Janet Smith",
                        "Diane Hicks",
                        "Beechnut",
                    ],
                    "trait": "other_collector",
                    "start": 0,
                    "end": 82,
                },
            ],
        )

    def test_collector_16(self):
        self.assertEqual(
            full_test("""Williams (Rocky) Gleason #F15GLEN55-B"""),
            [
                {
                    "collector_no": "F15GLEN55-B",
                    "collector": "Williams (Rocky) Gleason",
                    "trait": "collector",
                    "start": 0,
                    "end": 37,
                },
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
                {
                    "other_collector": [
                        "Dixie Damrel",
                        "Sarah Hunkins",
                        "Steven and Johan LaMoure",
                    ],
                    "trait": "other_collector",
                    "start": 0,
                    "end": 59,
                },
            ],
        )

    def test_collector_18(self):
        self.assertEqual(
            full_test("""Frederick H. Utech 91-1178"""),
            [
                {
                    "collector_no": "91-1178",
                    "collector": "Frederick H. Utech",
                    "trait": "collector",
                    "start": 0,
                    "end": 26,
                },
            ],
        )

    def test_collector_19(self):
        self.assertEqual(
            full_test("""A A.C. Saunders 39141"""),
            [
                {
                    "collector_no": "39141",
                    "collector": "A A.C. Saunders",
                    "trait": "collector",
                    "start": 0,
                    "end": 21,
                },
            ],
        )

    def test_collector_20(self):
        self.assertEqual(
            full_test("""purple. A A.C. Saunders 39141 14 Apr 2011"""),
            [
                {
                    "collector_no": "39141",
                    "collector": "A A.C. Saunders",
                    "trait": "collector",
                    "start": 8,
                    "end": 29,
                },
                {"date": "2011-04-14", "end": 41, "start": 30, "trait": "date"},
            ],
        )

    def test_collector_21(self):
        """It handles names with mixed case letters."""
        self.assertEqual(
            full_test("""Wendy McClure 2018-2"""),
            [
                {
                    "collector_no": "2018-2",
                    "collector": "Wendy McClure",
                    "trait": "collector",
                    "start": 0,
                    "end": 20,
                },
            ],
        )

    def test_collector_22(self):
        """It handles a taxon next to a name."""
        self.assertEqual(
            full_test("""Associated species: Neptunia gracilis G. Rink 7075"""),
            [
                {
                    "assoc_taxon_label": "associated species",
                    "trait": "assoc_taxon_label",
                    "start": 0,
                    "end": 18,
                },
                {
                    "rank": "species",
                    "trait": "associated_taxon",
                    "start": 20,
                    "end": 37,
                    "associated_taxon": "Neptunia gracilis",
                },
                {
                    "collector": "G. Rink",
                    "collector_no": "7075",
                    "trait": "collector",
                    "start": 38,
                    "end": 50,
                },
            ],
        )

    def test_collector_23(self):
        """It handles a taxon next to a name."""
        self.assertEqual(
            full_test("""collected by Merle Dortmond The University"""),
            [
                {
                    "collector": "Merle Dortmond",
                    "trait": "collector",
                    "start": 0,
                    "end": 27,
                },
            ],
        )

    def test_collector_24(self):
        """It handles a person after a taxon."""
        self.assertEqual(
            full_test(
                """Associated Species: Cephalanthus occidentalis Cass Blodgett 829"""
            ),
            [
                {
                    "assoc_taxon_label": "associated species",
                    "trait": "assoc_taxon_label",
                    "start": 0,
                    "end": 18,
                },
                {
                    "rank": "species",
                    "trait": "associated_taxon",
                    "start": 20,
                    "end": 45,
                    "associated_taxon": "Cephalanthus occidentalis",
                },
                {
                    "collector": "Cass Blodgett",
                    "collector_no": "829",
                    "trait": "collector",
                    "start": 46,
                    "end": 63,
                },
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
                {
                    "collector": ["W. Hess", "K. Allen", "K. Weise", "S. Peterson"],
                    "trait": "collector",
                    "start": 20,
                    "end": 73,
                }
            ],
        )

    def test_collector_27(self):
        """It handles a collector separated from their collector number."""
        self.assertEqual(
            full_test(
                """Little Belt Mountains J.B. Scammons Elevation: 5800 ft.
                No, 105 July 6, 1956"""
            ),
            [
                {
                    "trait": "collector",
                    "start": 22,
                    "end": 35,
                    "collector": "J.B. Scammons",
                    "collector_no": "105",
                },
                {
                    "elevation": 1767.84,
                    "units": "m",
                    "trait": "elevation",
                    "start": 36,
                    "end": 54,
                },
                {
                    "collector": "J.B. Scammons",
                    "trait": "collector_no",
                    "start": 56,
                    "end": 63,
                    "collector_no": "105",
                },
                {"date": "1956-07-06", "trait": "date", "start": 64, "end": 76},
            ],
        )

    def test_collector_28(self):
        """It handles a collector with number and a other collectors."""
        self.assertEqual(
            full_test("""Joshua R. Campbell 327 w/ S. Dickman"""),
            [
                {
                    "collector": "Joshua R. Campbell",
                    "trait": "collector",
                    "start": 0,
                    "end": 22,
                    "collector_no": "327",
                },
                {
                    "other_collector": ["S. Dickman"],
                    "trait": "other_collector",
                    "start": 23,
                    "end": 36,
                },
            ],
        )

    def test_collector_29(self):
        """It handles a collector with number and a other collectors."""
        self.assertEqual(
            full_test("""with Bob Simmons, Dana Griffin & Tom Morris"""),
            [
                {
                    "other_collector": ["Bob Simmons", "Dana Griffin", "Tom Morris"],
                    "trait": "other_collector",
                    "start": 0,
                    "end": 43,
                },
            ],
        )

    def test_collector_30(self):
        self.assertEqual(
            full_test("""With: Cindy Smith, Scott Rowan Sponsored by"""),
            [
                {
                    "other_collector": ["Cindy Smith", "Scott Rowan"],
                    "trait": "other_collector",
                    "start": 0,
                    "end": 30,
                },
            ],
        )

    def test_collector_31(self):
        self.assertEqual(
            full_test("""Joni Ward 866-a"""),
            [
                {
                    "collector": "Joni Ward",
                    "trait": "collector",
                    "collector_no": "866-a",
                    "start": 0,
                    "end": 15,
                },
            ],
        )

    def test_collector_32(self):
        self.assertEqual(
            full_test("""Cole Larsson-Whittaker 866-a"""),
            [
                {
                    "collector": "Cole Larsson-Whittaker",
                    "trait": "collector",
                    "collector_no": "866-a",
                    "start": 0,
                    "end": 28,
                },
            ],
        )

    def test_collector_33(self):
        self.assertEqual(
            full_test("""Collectors: Avena Nelson, Elias Nelson."""),
            [
                {
                    "collector": ["Avena Nelson", "Elias Nelson"],
                    "trait": "collector",
                    "start": 0,
                    "end": 38,
                },
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
                {
                    "taxon": "Mimosa sensitiva",
                    "rank": "species",
                    "trait": "taxon",
                    "start": 0,
                    "end": 16,
                },
                {"collector": "E. Mohr", "trait": "collector", "start": 17, "end": 38},
            ],
        )

    def test_collector_37(self):
        self.assertEqual(
            full_test(
                """
                with Juan Kaplan, Helena Walker Herbarium of a Botanical Garden"""
            ),
            [
                {
                    "other_collector": ["Juan Kaplan", "Helena Walker"],
                    "trait": "other_collector",
                    "start": 0,
                    "end": 31,
                }
            ],
        )

    def test_collector_38(self):
        self.assertEqual(
            full_test("""4 September 2008 J. Johnson with M. King Herbarium"""),
            [
                {
                    "date": "2008-09-04",
                    "trait": "date",
                    "start": 0,
                    "end": 16,
                },
                {
                    "collector": "J. Johnson",
                    "trait": "collector",
                    "start": 17,
                    "end": 27,
                },
                {
                    "other_collector": ["M. King"],
                    "trait": "other_collector",
                    "start": 28,
                    "end": 40,
                },
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
                {
                    "collector": "H. Richey",
                    "trait": "collector",
                    "collector_no": "HR1998-01",
                    "start": 0,
                    "end": 19,
                },
            ],
        )

    def test_collector_40(self):
        self.assertEqual(
            full_test("""AC Saunders 34380 OS"""),
            [
                {
                    "collector": "AC Saunders",
                    "trait": "collector",
                    "collector_no": "34380",
                    "start": 0,
                    "end": 17,
                },
            ],
        )

    # def test_collector_41(self):
    #     self.assertEqual(
    #         full_test(
    #             """Wendy Hodgson 8937 with Arts and Barb Phillips, Hualapai Elders"""
    #         ),
    #         [{'collector': 'Wendy Hodgson',
    #           'collector_no': '8937',
    #           'trait': 'collector',
    #           'start': 0,
    #           'end': 18},
    #          {'other_collector': ['Arts and Barb Phillips', 'Hualapai Elders'],
    #           'trait': 'other_collector',
    #           'start': 19,
    #           'end': 63}]
    #     )
