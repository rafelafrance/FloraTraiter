from dataclasses import asdict, dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class TaxonLike(Base):
    # Class vars ----------
    taxon_like_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "taxon_like_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(taxon_like_csv, "replace")

    taxon_labels: ClassVar[list[str]] = ["taxon", "multi_taxon"]
    # ---------------------

    taxon_like: str | list[str] = None
    relation: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        likes = self.taxon_like
        likes = likes if isinstance(likes, list) else [likes]
        for like in likes:
            dwc.add(**{self.key: {self.relation: like}})
        return dwc

    @property
    def key(self) -> str:
        return "associatedTaxa"

    @classmethod
    def pipe(cls, nlp: Language):
        with nlp.select_pipes(enable="tokenizer"):
            add.term_pipe(nlp, name="taxon_like_terms", path=cls.taxon_like_csv)

        add.trait_pipe(
            nlp,
            name="taxon_like_patterns",
            compiler=cls.taxon_like_patterns(),
            overwrite=[*cls.taxon_labels, "similar"],
        )
        add.cleanup_pipe(nlp, name="taxon_like_cleanup")

    @classmethod
    def taxon_like_patterns(cls):
        return Compiler(
            label="taxon_like",
            on_match="taxon_like_match",
            keep="taxon_like",
            decoder={
                "any": {},
                "prep": {"POS": {"IN": ["ADP", "CCONJ"]}},
                "similar": {"ENT_TYPE": "similar"},
                "taxon": {"ENT_TYPE": {"IN": cls.taxon_labels}},
            },
            patterns=[
                "similar+ taxon+",
                "similar+ any? prep taxon+",
            ],
        )

    @classmethod
    def taxon_like_match(cls, ent):
        data = next(
            (asdict(e._.trait) for e in ent.ents if e.label_ in cls.taxon_labels),
            {},
        )
        taxon_like = data["taxon"]
        similar = [t.text.lower() for t in ent if t._.term == "similar"]
        relation = " ".join(similar)
        return cls.from_ent(ent, taxon_like=taxon_like, relation=relation)


@registry.misc("taxon_like_match")
def taxon_like_match(ent):
    return TaxonLike.taxon_like_match(ent)
