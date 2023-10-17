from dataclasses import dataclass
from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from .base import Base

ALL_CSVS = [
    Path(__file__).parent / "terms" / "duration_terms.csv",
    Path(__file__).parent / "terms" / "flower_location_terms.csv",
    Path(__file__).parent / "terms" / "flower_morphology_terms.csv",
    Path(__file__).parent / "terms" / "formula_terms.csv",
    Path(__file__).parent / "terms" / "leaf_duration_terms.csv",
    Path(__file__).parent / "terms" / "leaf_folding_terms.csv",
    Path(__file__).parent / "terms" / "morphology_terms.csv",
    Path(__file__).parent / "terms" / "odor_terms.csv",
    Path(__file__).parent / "terms" / "plant_duration_terms.csv",
    Path(__file__).parent / "terms" / "reproduction_terms.csv",
    Path(__file__).parent / "terms" / "sex_terms.csv",
    Path(__file__).parent / "terms" / "venation_terms.csv",
    Path(__file__).parent / "terms" / "woodiness_terms.csv",
]

REPLACE = term_util.term_data(ALL_CSVS, "replace")
LABELS = term_util.get_labels(ALL_CSVS)


def build(nlp: Language):
    add.term_pipe(nlp, name="misc_terms", path=ALL_CSVS)
    add.trait_pipe(
        nlp, name="misc_patterns", compiler=misc_patterns(), overwrite=LABELS
    )
    # No cleanup here, we want the traits to hang around to help build other traits


def misc_patterns():
    return [
        Compiler(
            label="misc",
            on_match="misc_match",
            keep=LABELS,
            decoder={
                "(": {"TEXT": {"IN": t_const.OPEN}},
                ")": {"TEXT": {"IN": t_const.CLOSE}},
                "term": {"ENT_TYPE": {"IN": LABELS}},
            },
            patterns=[
                "  term ",
                "( term )",
            ],
        ),
    ]


@dataclass()
class Misc(Base):
    duration: str = None
    flower_location: str = None
    flower_morphology: str = None
    formula: str = None
    leaf_duration: str = None
    leaf_folding: str = None
    morphology: str = None
    odor: str = None
    plant_duration: str = None
    reproduction: str = None
    sex: str = None
    venation: str = None
    woodiness: str = None

    @classmethod
    def misc_match(cls, ent):
        frags = []
        relabel = ""
        for token in ent:
            relabel = token._.term
            if token.text not in "[]()":
                frags.append(REPLACE.get(token.lower_, token.lower_))

        ent._.relabel = relabel

        data = {relabel: " ".join(frags)}
        trait = cls.from_ent(ent, **data)

        return trait


@registry.misc("misc_match")
def misc_match(ent):
    return Misc.misc_match(ent)
