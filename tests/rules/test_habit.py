import unittest

from flora.pylib.rules.habit import Habit
from flora.pylib.rules.part import Part
from flora.pylib.rules.plant_duration import PlantDuration
from flora.pylib.rules.woodiness import Woodiness
from tests.setup import parse


class TestHabit(unittest.TestCase):
    def test_habit_01(self):
        self.assertEqual(
            parse("Stems often caespitose"),
            [
                Part(part="stem", trait="part", start=0, end=5, type="plant_part"),
                Habit(
                    habit="cespitose",
                    trait="habit",
                    start=12,
                    end=22,
                ),
            ],
        )

    def test_habit_02(self):
        self.maxDiff = None
        self.assertEqual(
            parse("Herbs perennial or subshrubs, epiphytic or epilithic."),
            [
                Woodiness(
                    woodiness="herb",
                    trait="woodiness",
                    start=0,
                    end=5,
                    part="shrub",
                ),
                PlantDuration(
                    plant_duration="perennial",
                    trait="plant_duration",
                    start=6,
                    end=15,
                ),
                Part(
                    part="shrub",
                    trait="part",
                    start=19,
                    end=28,
                    type="plant_part",
                ),
                Habit(habit="epiphytic", trait="habit", start=30, end=39),
                Habit(habit="epilithic", trait="habit", start=43, end=52),
            ],
        )
