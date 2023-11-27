import unittest

from flora.pylib.rules.id_number import IdNumber
from tests.setup import parse


class TestCollector(unittest.TestCase):
    def test_collector_01(self):
        self.assertEqual(
            parse("""No. 5595"""),
            [
                IdNumber(
                    trait="id_number",
                    number="5595",
                    type="record_number",
                    has_label=True,
                    start=0,
                    end=8,
                ),
            ],
        )

    def test_collector_02(self):
        self.assertEqual(
            parse("""Acc. No: 39"""),
            [
                IdNumber(
                    trait="id_number",
                    number="39",
                    type="accession_number",
                    has_label=True,
                    start=0,
                    end=11,
                ),
            ],
        )

    def test_collector_03(self):
        self.assertEqual(
            parse("""Col No 39"""),
            [
                IdNumber(
                    trait="id_number",
                    number="39",
                    type="collector_id",
                    has_label=True,
                    start=0,
                    end=9,
                ),
            ],
        )
