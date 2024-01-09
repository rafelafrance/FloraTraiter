import unittest
from datetime import date

from dateutil.relativedelta import relativedelta

from tests.setup import parse
from traiter.traiter.pylib.rules.date_ import Date


class TestDate(unittest.TestCase):
    def test_date_01(self):
        """It handles a date with a month name in the middle."""
        self.assertEqual(
            parse("""11 May 2004"""),
            [
                Date(
                    date="2004-05-11",
                    trait="date",
                    start=0,
                    end=11,
                ),
            ],
        )

    def test_date_02(self):
        """It handles a date with a month name in the middle and a 2-digit year."""
        self.assertEqual(
            parse("11 may 04"),
            [
                Date(
                    date="2004-05-11",
                    trait="date",
                    start=0,
                    end=9,
                ),
            ],
        )

    def test_date_03(self):
        """It adjusts future dates back a century for a 2-digit year."""
        tomorrow = date.today() + relativedelta(days=1)
        tomorrow = tomorrow.strftime("%d %b %y")
        expect = date.today() + relativedelta(years=-100, days=1)
        expect = expect.strftime("%Y-%m-%d")
        self.assertEqual(
            parse(tomorrow),
            [
                Date(
                    date=expect,
                    century_adjust=True,
                    trait="date",
                    start=0,
                    end=9,
                ),
            ],
        )

    def test_date_04(self):
        """It handles noise prior to parsing the date."""
        self.assertEqual(
            parse("No.: 113,306 Date: 8 October 1989"),
            [
                Date(
                    date="1989-10-08",
                    trait="date",
                    start=13,
                    end=33,
                ),
            ],
        )

    def test_date_05(self):
        """It handles an all numeric date."""
        self.assertEqual(
            parse("11-0297 10/20/2011"),
            [
                Date(
                    date="2011-10-20",
                    trait="date",
                    start=8,
                    end=18,
                ),
            ],
        )

    def test_date_06(self):
        """It handles noise in the separators."""
        self.assertEqual(
            parse("Collected by D, M, MOORE — Date AUG-_11,1968"),
            [
                Date(
                    date="1968-08-11",
                    trait="date",
                    start=27,
                    end=44,
                ),
            ],
        )

    def test_date_07(self):
        """It handles slashes between the date parts."""
        self.assertEqual(
            parse("""Date 8/20/75"""),
            [
                Date(
                    date="1975-08-20",
                    trait="date",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_date_08(self):
        """It handles dates missing a day part (numeric)."""
        self.assertEqual(
            parse("Andrew Jenkins 631 2/2010"),
            [
                Date(
                    date="2010-02",
                    missing_day=True,
                    trait="date",
                    start=19,
                    end=25,
                ),
            ],
        )

    def test_date_09(self):
        """It does not parse a bad date."""
        self.assertEqual(
            parse("Date Oct. 6, 197"),
            [],
        )

    def test_date_10(self):
        """It handles a bad month."""
        self.assertEqual(
            parse("June, 1992"),
            [
                Date(
                    date="1992-06",
                    trait="date",
                    missing_day=True,
                    start=0,
                    end=10,
                ),
            ],
        )

    def test_date_11(self):
        """It handles an abbreviated month."""
        self.assertEqual(
            parse("14 Jan. 1987"),
            [
                Date(
                    date="1987-01-14",
                    trait="date",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_date_12(self):
        """It skips a list of numbers."""
        self.assertEqual(
            parse("2 8 10"),
            [],
        )

    def test_date_13(self):
        """It allows the 'yy notation."""
        self.assertEqual(
            parse("Date: 6/30 '66"),
            [
                Date(
                    century_adjust=True,
                    date="1966-06-30",
                    trait="date",
                    start=0,
                    end=14,
                ),
            ],
        )

    def test_date_14(self):
        """It handles an abbreviated month."""
        self.assertEqual(
            parse("14 jan. 1987"),
            [
                Date(
                    date="1987-01-14",
                    trait="date",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_date_15(self):
        """It handles an abbreviated month."""
        self.assertEqual(
            parse("14 JAN. 1987"),
            [
                Date(
                    date="1987-01-14",
                    trait="date",
                    start=0,
                    end=12,
                ),
            ],
        )

    def test_date_16(self):
        """It handles month first."""
        self.assertEqual(
            parse("W May 19, 1998 HR1998-01"),
            [
                Date(
                    date="1998-05-19",
                    trait="date",
                    start=2,
                    end=14,
                ),
            ],
        )

    def test_date_17(self):
        self.assertEqual(
            parse("5/26/03,"),
            [
                Date(
                    date="2003-05-26",
                    trait="date",
                    start=0,
                    end=7,
                ),
            ],
        )

    def test_date_18(self):
        self.assertEqual(
            parse("Date: 10.Oct.70"),
            [
                Date(
                    century_adjust=True,
                    date="1970-10-10",
                    trait="date",
                    start=0,
                    end=15,
                ),
            ],
        )

    def test_date_19(self):
        self.assertEqual(
            parse("Date 30-VII-1977"),
            [
                Date(
                    date="1977-07-30",
                    trait="date",
                    start=0,
                    end=16,
                ),
            ],
        )

    def test_date_20(self):
        self.assertEqual(
            parse("SOFT. 3, 1899."),
            [
                Date(
                    date="1899-09-03",
                    trait="date",
                    start=0,
                    end=13,
                ),
            ],
        )

    def test_date_21(self):
        self.assertEqual(
            parse("± 4 x 3 mm."),
            [],
        )

    def test_date_22(self):
        self.assertEqual(
            parse("20091 19 X 1998"),
            [
                Date(
                    date="1998-10-19",
                    trait="date",
                    start=6,
                    end=15,
                ),
            ],
        )
