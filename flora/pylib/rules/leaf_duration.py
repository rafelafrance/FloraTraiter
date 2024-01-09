from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from flora.pylib.trait_util import clean_trait

from .linkable import Linkable


@dataclass(eq=False)
class LeafDuration(Linkable):
    # Class vars ----------
    leaf_duration_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "leaf_duration_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(
        leaf_duration_csv,
        "replace",
    )
    # ---------------------

    leaf_duration: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.leaf_duration})

    @property
    def key(self) -> str:
        return self.key_builder("leaf", "duration")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="leaf_duration_terms", path=cls.leaf_duration_csv)
        add.trait_pipe(
            nlp,
            name="leaf_duration_patterns",
            compiler=cls.leaf_duration_patterns(),
            overwrite=["leaf_duration"],
        )
        add.cleanup_pipe(nlp, name="leaf_duration_cleanup")

    @classmethod
    def leaf_duration_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "leaf_duration": {"ENT_TYPE": "leaf_duration"},
        }
        return [
            Compiler(
                label="leaf_duration",
                on_match="leaf_duration_match",
                keep="leaf_duration",
                decoder=decoder,
                patterns=[
                    "  leaf_duration ",
                    "( leaf_duration )",
                ],
            ),
        ]

    @classmethod
    def leaf_duration_match(cls, ent):
        return cls.from_ent(ent, leaf_duration=clean_trait(ent, cls.replace))


@registry.misc("leaf_duration_match")
def leaf_duration_match(ent):
    return LeafDuration.leaf_duration_match(ent)
