from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from ..trait_util import clean_trait
from .linkable import Linkable


@dataclass
class LeafFolding(Linkable):
    # Class vars ----------
    leaf_folding_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "leaf_folding_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(leaf_folding_csv, "replace")
    # ---------------------

    leaf_folding: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="leaf_folding_terms", path=cls.leaf_folding_csv)
        add.trait_pipe(
            nlp,
            name="leaf_folding_patterns",
            compiler=cls.leaf_folding_patterns(),
            overwrite=["leaf_folding"],
        )
        add.cleanup_pipe(nlp, name="leaf_folding_cleanup")

    @classmethod
    def leaf_folding_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "leaf_folding": {"ENT_TYPE": "leaf_folding"},
        }
        return [
            Compiler(
                label="leaf_folding",
                on_match="leaf_folding_match",
                keep="leaf_folding",
                decoder=decoder,
                patterns=[
                    "  leaf_folding ",
                    "( leaf_folding )",
                ],
            ),
        ]

    @classmethod
    def leaf_folding_match(cls, ent):
        return cls.from_ent(ent, leaf_folding=clean_trait(ent, cls.replace))


@registry.misc("leaf_folding_match")
def leaf_folding_match(ent):
    return LeafFolding.leaf_folding_match(ent)
