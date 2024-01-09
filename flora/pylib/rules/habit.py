from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class Habit(Base):
    # Class vars ----------
    all_csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "habit_terms.csv",
        Path(__file__).parent / "terms" / "shape_terms.csv",
    ]
    replace: ClassVar[dict[str, str]] = term_util.term_data(all_csvs, "replace")
    # ---------------------

    habit: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(habit=self.habit)

    @property
    def key(self) -> str:
        return self.key_builder("habit")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="habit_terms", path=cls.all_csvs)
        add.trait_pipe(nlp, name="habit_patterns", compiler=cls.habit_patterns())
        add.cleanup_pipe(nlp, name="habit_cleanup")

    @classmethod
    def habit_patterns(cls):
        return [
            Compiler(
                label="habit",
                on_match="habit_match",
                keep="habit",
                decoder={
                    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
                    "habit": {"ENT_TYPE": "habit_term"},
                    "shape": {"ENT_TYPE": "shape"},
                    "tree": {"ENT_TYPE": "habit_tree"},
                },
                patterns=[
                    "habit",
                    "shape -? tree",
                ],
            ),
        ]

    @classmethod
    def habit_match(cls, ent):
        frags = [cls.replace.get(t.lower_, t.lower_) for t in ent]
        return cls.from_ent(ent, habit=" ".join(frags))


@registry.misc("habit_match")
def habit_match(ent):
    return Habit.habit_match(ent)
