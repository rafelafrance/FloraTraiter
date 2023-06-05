import re
from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

SHAPE_CSV = Path(__file__).parent / "terms" / "shape_terms.csv"
SHAPE_LOC = ["shape_term", "shape_leader", "location"]
REPLACE = term_util.term_data(SHAPE_CSV, "replace")


def build(nlp: Language):
    add.term_pipe(nlp, name="shape_terms", path=SHAPE_CSV)
    add.trait_pipe(
        nlp, name="shape_patterns", compiler=shape_patterns(), overwrite=["count"]
    )
    add.cleanup_pipe(nlp, name="shape_cleanup")


def shape_patterns():
    return [
        Compiler(
            label="shape",
            on_match="shape_match",
            keep="shape",
            decoder={
                "-": {"TEXT": {"IN": t_const.DASH}},
                "-/to": {"LOWER": {"IN": t_const.DASH + ["to", "_"]}},
                "9": {"IS_DIGIT": True},
                "angular": {"LOWER": {"IN": ["angular", "angulate"]}},
                "shape": {"ENT_TYPE": "shape_term"},
                "shape_leader": {"ENT_TYPE": "shape_leader"},
                "shape_loc": {"ENT_TYPE": {"IN": SHAPE_LOC}},
                "shape_word": {"ENT_TYPE": {"IN": ["shape_term", "shape_leader"]}},
            },
            patterns=[
                "shape_loc*   -*    shape+",
                "shape_loc*   -*    shape       -* shape+",
                "shape_leader -/to+ shape_word+ -* shape+",
                "shape_word+  -*    shape+",
                "shape_loc* 9 -     angular",
            ],
        ),
    ]


@registry.misc("shape_match")
def shape_match(ent):

    # Handle 3-angular etc.
    if re.match(r"^\d", ent.text):
        shape = "polygonal"

    # All other shapes
    else:
        shape = {}  # Dicts preserve order sets do not
        for token in ent:
            if token._.term == "shape_term" and token.text != "-":
                word = REPLACE.get(token.lower_, token.lower_)
                shape[word] = 1
        shape = "-".join(shape)
        shape = REPLACE.get(shape, shape)

    ent._.data = {"shape": shape}
