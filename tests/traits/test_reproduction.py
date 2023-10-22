import unittest

from flora.pylib.traits.part import Part
from flora.pylib.traits.reproduction import Reproduction
from flora.pylib.traits.sex import Sex
from tests.setup import test


class TestReproduction(unittest.TestCase):
    def test_reproduction_01(self):
        self.maxDiff = None
        self.assertEqual(
            test(
                """
                bisexual (unisexual and plants sometimes gynodioecious,
                or plants dioecious"""
            ),
            [
                Sex(sex="bisexual", trait="sex", start=0, end=8),
                Sex(sex="unisexual", trait="sex", start=10, end=19),
                Part(
                    trait="part",
                    part="plant",
                    type="plant_part",
                    sex="unisexual",
                    start=24,
                    end=30,
                ),
                Reproduction(
                    reproduction="gynodioecious",
                    trait="reproduction",
                    start=41,
                    end=54,
                ),
                Part(
                    type="plant_part",
                    trait="part",
                    part="plant",
                    sex="unisexual",
                    start=59,
                    end=65,
                ),
                Reproduction(
                    reproduction="dioecious",
                    trait="reproduction",
                    start=66,
                    end=75,
                ),
            ],
        )
