from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

SURFACE_CSV = Path(__file__).parent / "terms" / "surface_terms.csv"
REPLACE = term_util.term_data(SURFACE_CSV, "replace")


def build(nlp: Language):
    add.term_pipe(nlp, name="surface_terms", path=SURFACE_CSV)
    add.trait_pipe(nlp, name="surface_patterns", compiler=surface_patterns())
    add.cleanup_pipe(nlp, name="surface_cleanup")


def surface_patterns():
    return [
        Compiler(
            label="surface",
            on_match="surface_match",
            keep="surface",
            decoder={
                "-": {"TEXT": {"IN": t_const.DASH}},
                "surface": {"ENT_TYPE": "surface_term"},
                "surface_leader": {"ENT_TYPE": "surface_leader"},
            },
            patterns=[
                "                  surface",
                "surface_leader -? surface",
            ],
        ),
    ]


@registry.misc("surface_match")
def surface_match(ent):
    surface = {}  # Dicts preserve order sets do not
    for token in ent:
        if token._.term == "surface_term" and token.text != "-":
            word = REPLACE.get(token.lower_, token.lower_)
            surface[word] = 1
    surface = " ".join(surface)
    surface = REPLACE.get(surface, surface)
    ent._.data = {"surface": surface}
