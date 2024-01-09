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
class FlowerLocation(Linkable):
    # Class vars ----------
    flower_location_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "flower_location_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(
        flower_location_csv,
        "replace",
    )
    # ---------------------

    flower_location: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.flower_location})

    @property
    def key(self) -> str:
        return self.key_builder("flower", "location")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="flower_location_terms", path=cls.flower_location_csv)
        add.trait_pipe(
            nlp,
            name="flower_location_patterns",
            compiler=cls.flower_location_patterns(),
            overwrite=["flower_location"],
        )
        add.cleanup_pipe(nlp, name="flower_location_cleanup")

    @classmethod
    def flower_location_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "flower_location": {"ENT_TYPE": "flower_location"},
        }
        return [
            Compiler(
                label="flower_location",
                on_match="flower_location_match",
                keep="flower_location",
                decoder=decoder,
                patterns=[
                    "  flower_location ",
                    "( flower_location )",
                ],
            ),
        ]

    @classmethod
    def flower_location_match(cls, ent):
        return cls.from_ent(ent, flower_location=clean_trait(ent, cls.replace))


@registry.misc("flower_location_match")
def flower_location_match(ent):
    return FlowerLocation.flower_location_match(ent)
