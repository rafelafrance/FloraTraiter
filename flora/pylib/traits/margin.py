from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

MARGIN_CSV = Path(__file__).parent / "terms" / "margin_terms.csv"

REPLACE = term_util.term_data(MARGIN_CSV, "replace")


def build(nlp: Language):
    add.term_pipe(nlp, name="margin_terms", path=MARGIN_CSV)
    add.trait_pipe(nlp, name="margin_patterns", compiler=margin_patterns())
    add.cleanup_pipe(nlp, name="margin_cleanup")


def margin_patterns():
    return [
        Compiler(
            label="margin",
            on_match="margin_match",
            keep="margin",
            decoder={
                "-": {"TEXT": {"IN": t_const.DASH}},
                "margin": {"ENT_TYPE": "margin_term"},
                "shape": {"ENT_TYPE": "shape"},
                "leader": {"ENT_TYPE": {"IN": ["shape", "margin_leader"]}},
                "follower": {"ENT_TYPE": {"IN": ["margin_term", "margin_follower"]}},
            },
            patterns=[
                "leader* -* margin+",
                "leader* -* margin -* follower*",
                "leader* -* margin -* shape? follower+ shape?",
                "shape+ -* follower+",
            ],
        ),
    ]


@registry.misc("margin_match")
def margin_match(ent):
    margin = {}  # Dicts preserve order sets do not
    for token in ent:
        if token._.term in ["margin_term", "shape"] and token.text != "-":
            word = REPLACE.get(token.lower_, token.lower_)
            margin[word] = 1
    margin = "-".join(margin.keys())
    margin = REPLACE.get(margin, margin)
    ent._.data = {"margin": margin}
