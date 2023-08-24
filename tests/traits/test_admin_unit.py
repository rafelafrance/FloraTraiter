import unittest

from tests.setup import test2


class TestAdminUnit(unittest.TestCase):
    def test_admin_unit_01(self):
        """It gets a county notation."""
        self.assertEqual(
            test2("""Hempstead County"""),
            [
                {
                    "us_county": "Hempstead",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 16,
                },
            ],
        )

    def test_admin_unit_02(self):
        """A label is required."""
        self.assertEqual(
            test2("""Watauga"""),
            [],
        )

    def test_admin_unit_03(self):
        """It handles a confusing county notation."""
        self.assertEqual(
            test2("""Flora of ARKANSAS County: MISSISSIPPI"""),
            [
                {
                    "us_county": "Mississippi",
                    "us_state": "Arkansas",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 37,
                },
            ],
        )

    def test_admin_unit_04(self):
        """It handles a county label before the county name."""
        self.assertEqual(
            test2("""COUNTY: Lee"""),
            [{"us_county": "Lee", "trait": "admin_unit", "start": 0, "end": 11}],
        )

    def test_admin_unit_05(self):
        """It handles a trailing county abbreviation."""
        self.assertEqual(
            test2("""Alleghany Co,"""),
            [
                {
                    "us_county": "Alleghany",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 12,
                },
            ],
        )

    def test_admin_unit_06(self):
        """It handles a state abbreviation."""
        self.assertEqual(
            test2("""Desha Co., Ark."""),
            [
                {
                    "us_state": "Arkansas",
                    "us_county": "Desha",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 15,
                }
            ],
        )

    def test_admin_unit_07(self):
        """It gets a state notation."""
        self.assertEqual(
            test2("""PLANTS OF ARKANSAS"""),
            [
                {
                    "us_state": "Arkansas",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 18,
                },
            ],
        )

    def test_admin_unit_08(self):
        """It gets a multi-word state notation."""
        self.assertEqual(
            test2("""PLANTS OF NORTH CAROLINA"""),
            [
                {
                    "us_state": "North Carolina",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 24,
                },
            ],
        )

    def test_admin_unit_09(self):
        """It gets a state notation separated from the county."""
        self.assertEqual(
            test2(
                """
                APPALACHIAN STATE UNIVERSITY HERBARIUM
                PLANTS OF NORTH CAROLINA
                STONE MOUNTAIN STATE PARK
                WILKES COUNTY
                """
            ),
            [
                {
                    "us_state": "North Carolina",
                    "trait": "admin_unit",
                    "start": 39,
                    "end": 63,
                },
                {
                    "us_county": "Wilkes",
                    "trait": "admin_unit",
                    "start": 90,
                    "end": 103,
                },
            ],
        )

    def test_admin_unit_10(self):
        """It parses multi-word counties and states."""
        self.assertEqual(
            test2("""Cape May, New Jersey"""),
            [
                {
                    "us_county": "Cape May",
                    "us_state": "New Jersey",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 20,
                },
            ],
        )

    def test_admin_unit_11(self):
        """County vs colorado (CO)."""
        self.assertEqual(
            test2("""ARCHULETA CO"""),
            [
                {
                    "us_county": "Archuleta",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 12,
                },
            ],
        )

    def test_admin_unit_12(self):
        """County vs colorado (CO)."""
        self.assertEqual(
            test2("""Archuleta CO"""),
            [
                {
                    "us_state": "Colorado",
                    "us_county": "Archuleta",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 12,
                },
            ],
        )

    def test_admin_unit_13(self):
        """It does not pick up label headers and footers."""
        self.assertEqual(
            test2("""The University of Georgia Athens, GA, U.S.A."""),
            [{"country": "USA", "end": 44, "start": 38, "trait": "admin_unit"}],
        )

    def test_admin_unit_14(self):
        """It does not pick up label headers and footers."""
        self.assertEqual(
            test2("""Tree The New York Botanical Garden Herbarium"""),
            [{"end": 4, "plant_part": "tree", "start": 0, "trait": "plant_part"}],
        )

    def test_admin_unit_15(self):
        self.assertEqual(
            test2("""St. Lucie Co.: Fort Pierce."""),
            [
                {
                    "us_county": "St. Lucie",
                    "trait": "admin_unit",
                    "start": 0,
                    "end": 13,
                },
                {
                    "locality": "Fort Pierce.",
                    "trait": "locality",
                    "start": 15,
                    "end": 27,
                },
            ],
        )
