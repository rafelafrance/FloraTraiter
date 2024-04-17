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
                Part(part="stem", start=0, end=5, type="plant_part"),
                Habit(
                    habit="cespitose",
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
                    start=0,
                    end=5,
                    part="shrub",
                ),
                PlantDuration(
                    plant_duration="perennial",
                    start=6,
                    end=15,
                ),
                Part(
                    part="shrub",
                    start=19,
                    end=28,
                    type="plant_part",
                ),
                Habit(habit="epiphytic", start=30, end=39),
                Habit(habit="epilithic", start=43, end=52),
            ],
        )
