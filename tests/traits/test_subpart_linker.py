import unittest

from tests.setup import test


class TestSubpartLinker(unittest.TestCase):
    def test_subpart_linker_01(self):
        self.assertEqual(
            test("""limbs (1-) 2-4 (-5) pairs;"""),
            [
                {"subpart": "limb", "trait": "subpart", "start": 0, "end": 5},
                {
                    "min": 1,
                    "low": 2,
                    "high": 4,
                    "max": 5,
                    "trait": "count",
                    "start": 6,
                    "end": 25,
                    "count_group": "pairs",
                    "subpart": "limb",
                },
            ],
        )

    def test_subpart_linker_02(self):
        self.assertEqual(
            test("""blades oblong setose-ciliolate"""),
            [
                {"leaf_part": "leaf", "trait": "leaf_part", "start": 0, "end": 6},
                {
                    "shape": "oblong",
                    "trait": "shape",
                    "subpart": "ciliolate",
                    "start": 7,
                    "end": 13,
                    "leaf_part": "leaf",
                },
                {
                    "surface": "setose",
                    "subpart": "ciliolate",
                    "trait": "surface",
                    "start": 14,
                    "end": 20,
                    "leaf_part": "leaf",
                },
                {
                    "subpart": "ciliolate",
                    "leaf_part": "leaf",
                    "trait": "subpart",
                    "start": 20,
                    "end": 30,
                },
            ],
        )
