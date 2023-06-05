from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

TAXON_LIKE_CSV = Path(__file__).parent / "terms" / "taxon_like_terms.csv"
REPLACE = term_util.term_data(TAXON_LIKE_CSV, "replace")

TAXON_LABELS = ["taxon", "multi_taxon"]


def build(nlp: Language):
    with nlp.select_pipes(enable="tokenizer"):
        add.term_pipe(nlp, name="taxon_like_terms", path=TAXON_LIKE_CSV)

    add.trait_pipe(
        nlp,
        name="taxon_like_patterns",
        compiler=taxon_like_patterns(),
        overwrite=[*TAXON_LABELS, "similar"],
    )
    add.cleanup_pipe(nlp, name="taxon_like_cleanup")


def taxon_like_patterns():
    return Compiler(
        label="taxon_like",
        on_match="taxon_like_match",
        keep="taxon_like",
        decoder={
            "any": {},
            "prep": {"POS": {"IN": ["ADP", "CCONJ"]}},
            "similar": {"ENT_TYPE": "similar"},
            "taxon": {"ENT_TYPE": {"IN": TAXON_LABELS}},
        },
        patterns=[
            "similar+ taxon+",
            "similar+ any? prep taxon+",
        ],
    )


@registry.misc("taxon_like_match")
def taxon_like_match(ent):
    ent._.data = next((e._.data for e in ent.ents if e.label_ in TAXON_LABELS), {})
    ent._.data["taxon_like"] = ent._.data["taxon"]
    del ent._.data["taxon"]
    similar = [t.text.lower() for t in ent if t._.term == "similar"]
    ent._.data["relation"] = " ".join(similar)
