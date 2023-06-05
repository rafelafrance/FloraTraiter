from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

HABIT_CSV = Path(__file__).parent / "terms" / "habit_terms.csv"
SHAPE_CSV = Path(__file__).parent / "terms" / "shape_terms.csv"
ALL_CSVS = [HABIT_CSV, SHAPE_CSV]

REPLACE = term_util.term_data(HABIT_CSV, "replace")


def build(nlp: Language):
    add.term_pipe(nlp, name="habit_terms", path=ALL_CSVS)
    add.trait_pipe(nlp, name="habit_patterns", compiler=habit_patterns())
    add.cleanup_pipe(nlp, name="habit_cleanup")


def habit_patterns():
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
        )
    ]


@registry.misc("habit_match")
def habit_match(ent):
    frags = [REPLACE.get(t.lower_, t.lower_) for t in ent]
    ent._.data = {"habit": " ".join(frags)}
