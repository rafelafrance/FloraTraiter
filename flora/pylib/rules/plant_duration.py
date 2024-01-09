from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base

from flora.pylib.trait_util import clean_trait


@dataclass(eq=False)
class PlantDuration(Base):
    # Class vars ----------
    plant_duration_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "plant_duration_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(
        plant_duration_csv,
        "replace",
    )
    # ---------------------

    plant_duration: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(plantDuration=self.plant_duration)

    @property
    def key(self) -> str:
        return "plantDuration"

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="plant_duration_terms", path=cls.plant_duration_csv)
        add.trait_pipe(
            nlp,
            name="plant_duration_patterns",
            compiler=cls.plant_duration_patterns(),
            overwrite=["plant_duration"],
        )
        add.cleanup_pipe(nlp, name="plant_duration_cleanup")

    @classmethod
    def plant_duration_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "plant_duration": {"ENT_TYPE": "plant_duration"},
        }
        return [
            Compiler(
                label="plant_duration",
                on_match="plant_duration_match",
                keep="plant_duration",
                decoder=decoder,
                patterns=[
                    "  plant_duration ",
                    "( plant_duration )",
                ],
            ),
        ]

    @classmethod
    def plant_duration_match(cls, ent):
        return cls.from_ent(ent, plant_duration=clean_trait(ent, cls.replace))


@registry.misc("plant_duration_match")
def plant_duration_match(ent):
    return PlantDuration.plant_duration_match(ent)
