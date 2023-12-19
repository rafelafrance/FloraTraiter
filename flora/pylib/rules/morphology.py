from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy import registry

from traiter.traiter.pylib import const as t_const
from traiter.traiter.pylib import term_util
from traiter.traiter.pylib.darwin_core import DarwinCore
from traiter.traiter.pylib.pattern_compiler import Compiler
from traiter.traiter.pylib.pipes import add
from traiter.traiter.pylib.rules.base import Base

from ..trait_util import clean_trait


@dataclass(eq=False)
class Morphology(Base):
    # Class vars ----------
    morphology_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "morphology_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(morphology_csv, "replace")
    # ---------------------

    morphology: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(morphology=self.morphology)

    @property
    def key(self) -> str:
        return "morphology"

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="morphology_terms", path=cls.morphology_csv)
        add.trait_pipe(
            nlp,
            name="morphology_patterns",
            compiler=cls.morphology_patterns(),
            overwrite=["morphology"],
        )
        add.cleanup_pipe(nlp, name="morphology_cleanup")

    @classmethod
    def morphology_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "morphology": {"ENT_TYPE": "morphology"},
        }
        return [
            Compiler(
                label="morphology",
                on_match="morphology_match",
                keep="morphology",
                decoder=decoder,
                patterns=[
                    "  morphology ",
                    "( morphology )",
                ],
            ),
        ]

    @classmethod
    def morphology_match(cls, ent):
        return cls.from_ent(ent, morphology=clean_trait(ent, cls.replace))


@registry.misc("morphology_match")
def morphology_match(ent):
    return Morphology.morphology_match(ent)
