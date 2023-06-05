import unittest

from tests.setup import test


class TestPartLocation(unittest.TestCase):
    def test_part_location_01(self):
        self.assertEqual(
            test("stipules 3-8 mm, semiamplexicaul, adnate to petiole for 1-2 mm"),
            [
                {"leaf_part": "stipule", "trait": "leaf_part", "start": 0, "end": 8},
                {
                    "dimensions": "length",
                    "length_low": 0.3,
                    "length_high": 0.8,
                    "trait": "size",
                    "start": 9,
                    "end": 15,
                    "units": "cm",
                    "leaf_part": "stipule",
                },
                {
                    "shape": "semiamplexicaul",
                    "trait": "shape",
                    "start": 17,
                    "end": 32,
                    "leaf_part": "stipule",
                },
                {
                    "part_as_distance": "adnate to petiole for 1 - 2 mm",
                    "trait": "part_as_distance",
                    "start": 34,
                    "end": 62,
                },
            ],
        )

    def test_part_location_02(self):
        self.assertEqual(
            test("leaves completely embracing stem but not connate"),
            [
                {
                    "leaf_part": "leaf",
                    "trait": "leaf_part",
                    "start": 0,
                    "end": 6,
                    "part_as_loc": "embracing stem",
                },
                {
                    "part_as_loc": "embracing stem",
                    "trait": "part_as_loc",
                    "start": 18,
                    "end": 32,
                },
            ],
        )

    def test_part_location_03(self):
        self.assertEqual(
            test("stipules shortly ciliate at margin"),
            [
                {
                    "leaf_part": "stipule",
                    "trait": "leaf_part",
                    "subpart_as_loc": "at margin",
                    "start": 0,
                    "end": 8,
                },
                {
                    "surface": "ciliate",
                    "trait": "surface",
                    "subpart_as_loc": "at margin",
                    "start": 9,
                    "end": 24,
                    "leaf_part": "stipule",
                },
                {
                    "subpart_as_loc": "at margin",
                    "trait": "subpart_as_loc",
                    "start": 25,
                    "end": 34,
                },
            ],
        )

    def test_part_location_04(self):
        self.assertEqual(
            test("the short terminal pseudoraceme"),
            [
                {
                    "inflorescence": "pseudoraceme",
                    "trait": "inflorescence",
                    "start": 19,
                    "end": 31,
                    "location": "terminal",
                },
            ],
        )

    def test_part_location_05(self):
        self.assertEqual(
            test("capitula immersed in foliage."),
            [
                {
                    "inflorescence": "capitulum",
                    "trait": "inflorescence",
                    "part_as_loc": "immersed in foliage",
                    "start": 0,
                    "end": 8,
                },
                {
                    "part_as_loc": "immersed in foliage",
                    "trait": "part_as_loc",
                    "start": 9,
                    "end": 28,
                },
            ],
        )

    def test_part_location_06(self):
        self.assertEqual(
            test(
                "the short terminal pseudoraceme of ovoid-ellipsoid or globose "
                "capitula immersed in foliage."
            ),
            [
                {
                    "inflorescence": "pseudoraceme",
                    "trait": "inflorescence",
                    "start": 19,
                    "end": 31,
                    "location": "terminal",
                },
                {
                    "shape": "ovoid-ellipsoid",
                    "trait": "shape",
                    "start": 35,
                    "end": 50,
                    "inflorescence": "pseudoraceme",
                    "location": "terminal",
                },
                {
                    "shape": "spheric",
                    "trait": "shape",
                    "start": 54,
                    "end": 61,
                    "inflorescence": "capitulum",
                    "part_as_loc": "immersed in foliage",
                },
                {
                    "inflorescence": "capitulum",
                    "trait": "inflorescence",
                    "start": 62,
                    "end": 70,
                    "part_as_loc": "immersed in foliage",
                },
                {
                    "part_as_loc": "immersed in foliage",
                    "trait": "part_as_loc",
                    "start": 71,
                    "end": 90,
                },
            ],
        )
