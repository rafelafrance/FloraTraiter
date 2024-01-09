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
class Duration(Linkable):
    # Class vars ----------
    duration_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "duration_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(duration_csv, "replace")
    # ---------------------

    duration: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.duration})

    @property
    def key(self) -> str:
        return self.key_builder("duration")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="duration_terms", path=cls.duration_csv)
        add.trait_pipe(
            nlp,
            name="duration_patterns",
            compiler=cls.duration_patterns(),
            overwrite=["duration"],
        )
        add.cleanup_pipe(nlp, name="duration_cleanup")

    @classmethod
    def duration_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "duration": {"ENT_TYPE": "duration"},
        }
        return [
            Compiler(
                label="duration",
                on_match="duration_match",
                keep="duration",
                decoder=decoder,
                patterns=[
                    "  duration ",
                    "( duration )",
                ],
            ),
        ]

    @classmethod
    def duration_match(cls, ent):
        return cls.from_ent(ent, duration=clean_trait(ent, cls.replace))


@registry.misc("duration_match")
def duration_match(ent):
    return Duration.duration_match(ent)
