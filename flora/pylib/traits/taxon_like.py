from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits.base import Base

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


@dataclass
class TaxonLike(Base):
    taxon_like: str | list[str] = None
    relation: str = None

    @classmethod
    def taxon_like_match(cls, ent):
        data = next(
            (asdict(e._.trait) for e in ent.ents if e.label_ in TAXON_LABELS),
            {},
        )
        taxon_like = data["taxon"]
        similar = [t.text.lower() for t in ent if t._.term == "similar"]
        relation = " ".join(similar)
        return cls.from_ent(ent, taxon_like=taxon_like, relation=relation)


@registry.misc("taxon_like_match")
def taxon_like_match(ent):
    return TaxonLike.taxon_like_match(ent)
