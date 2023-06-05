import unittest

from tests.setup import test


class TestMargin(unittest.TestCase):
    def test_margin_00(self):
        test("""margins coarsely toothed or remotely sinuate-dentate to serrate,""")

    def test_margin_01(self):
        self.assertEqual(
            test("margin shallowly undulate-crenate"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 6},
                {
                    "margin": "undulate-crenate",
                    "trait": "margin",
                    "subpart": "margin",
                    "start": 7,
                    "end": 33,
                },
            ],
        )

    def test_margin_02(self):
        self.assertEqual(
            test("reniform, undulate-margined"),
            [
                {"shape": "reniform", "trait": "shape", "start": 0, "end": 8},
                {
                    "margin": "undulate",
                    "trait": "margin",
                    "start": 10,
                    "end": 27,
                },
            ],
        )

    def test_margin_03(self):
        self.assertEqual(
            test("margins thickened-corrugated"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 7},
                {
                    "margin": "corrugated",
                    "trait": "margin",
                    "subpart": "margin",
                    "start": 8,
                    "end": 28,
                },
            ],
        )

    def test_margin_04(self):
        self.assertEqual(
            test("margins coarsely toothed or remotely sinuate-dentate to serrate,"),
            [
                {"subpart": "margin", "trait": "subpart", "start": 0, "end": 7},
                {
                    "margin": "toothed",
                    "trait": "margin",
                    "subpart": "margin",
                    "start": 8,
                    "end": 24,
                },
                {
                    "margin": "sinuate-dentate",
                    "trait": "margin",
                    "subpart": "margin",
                    "start": 28,
                    "end": 52,
                },
                {
                    "margin": "serrate",
                    "trait": "margin",
                    "subpart": "margin",
                    "start": 56,
                    "end": 63,
                },
            ],
        )
