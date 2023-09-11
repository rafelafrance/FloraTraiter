import unittest

from tests.setup import full_test


class TestAdminUnit(unittest.TestCase):
    def test_admin_unit_01(self):
        """It gets a county notation."""
        self.assertEqual(
            full_test("""Hempstead County"""),
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
            full_test("""Watauga"""),
            [],
        )

    def test_admin_unit_03(self):
        """It handles a confusing county notation."""
        self.assertEqual(
            full_test("""Flora of ARKANSAS County: MISSISSIPPI"""),
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
            full_test("""COUNTY: Lee"""),
            [{"us_county": "Lee", "trait": "admin_unit", "start": 0, "end": 11}],
        )

    def test_admin_unit_05(self):
        """It handles a trailing county abbreviation."""
        self.assertEqual(
            full_test("""Alleghany Co,"""),
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
            full_test("""Desha Co., Ark."""),
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
            full_test("""PLANTS OF ARKANSAS"""),
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
            full_test("""PLANTS OF NORTH CAROLINA"""),
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
            full_test(
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
            full_test("""Cape May, New Jersey"""),
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
            full_test("""ARCHULETA CO"""),
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
            full_test("""Archuleta CO"""),
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
            full_test("""The University of Georgia Athens, GA, U.S.A."""),
            [{"country": "USA", "end": 44, "start": 38, "trait": "admin_unit"}],
        )

    def test_admin_unit_14(self):
        """It does not pick up label headers and footers."""
        self.assertEqual(
            full_test("""Tree The New York Botanical Garden Herbarium"""),
            [{"end": 4, "plant_part": "tree", "start": 0, "trait": "plant_part"}],
        )

    def test_admin_unit_15(self):
        self.assertEqual(
            full_test("""St. Lucie Co.: Fort Pierce."""),
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

    def test_admin_unit_16(self):
        """It gets a province."""
        self.assertEqual(
            full_test("""Province of Panama"""),
            [{"end": 18, "province": "panama", "start": 0, "trait": "admin_unit"}],
        )

    def test_admin_unit_17(self):
        """It gets state county notation on two lines."""
        self.assertEqual(
            full_test(
                """
                Herbarium of the University of North Carolina
                SOUTH CAROLINA
                Dillon County
                """
            ),
            [
                {
                    "us_state": "South Carolina",
                    "us_county": "Dillon",
                    "trait": "admin_unit",
                    "start": 46,
                    "end": 74,
                }
            ],
        )
