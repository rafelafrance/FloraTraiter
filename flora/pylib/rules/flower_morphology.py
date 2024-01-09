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
class FlowerMorphology(Linkable):
    # Class vars ----------
    flower_morphology_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "flower_morphology_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(
        flower_morphology_csv,
        "replace",
    )
    # ---------------------

    flower_morphology: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.flower_morphology})

    @property
    def key(self) -> str:
        return self.key_builder("flower", "morphology")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(
            nlp,
            name="flower_morphology_terms",
            path=cls.flower_morphology_csv,
        )
        add.trait_pipe(
            nlp,
            name="flower_morphology_patterns",
            compiler=cls.flower_morphology_patterns(),
            overwrite=["flower_morphology"],
        )
        add.cleanup_pipe(nlp, name="flower_morphology_cleanup")

    @classmethod
    def flower_morphology_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "flower_morphology": {"ENT_TYPE": "flower_morphology"},
        }
        return [
            Compiler(
                label="flower_morphology",
                on_match="flower_morphology_match",
                keep="flower_morphology",
                decoder=decoder,
                patterns=[
                    "  flower_morphology ",
                    "( flower_morphology )",
                ],
            ),
        ]

    @classmethod
    def flower_morphology_match(cls, ent):
        return cls.from_ent(ent, flower_morphology=clean_trait(ent, cls.replace))


@registry.misc("flower_morphology_match")
def flower_morphology_match(ent):
    return FlowerMorphology.flower_morphology_match(ent)
