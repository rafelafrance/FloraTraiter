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
class Reproduction(Base):
    # Class vars ----------
    reproduction_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "reproduction_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(reproduction_csv, "replace")
    # ---------------------

    reproduction: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(reproduction=self.reproduction)

    @property
    def key(self) -> str:
        return "reproduction"

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="reproduction_terms", path=cls.reproduction_csv)
        add.trait_pipe(
            nlp,
            name="reproduction_patterns",
            compiler=cls.reproduction_patterns(),
            overwrite=["reproduction"],
        )
        add.cleanup_pipe(nlp, name="reproduction_cleanup")

    @classmethod
    def reproduction_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "reproduction": {"ENT_TYPE": "reproduction"},
        }
        return [
            Compiler(
                label="reproduction",
                on_match="reproduction_match",
                keep="reproduction",
                decoder=decoder,
                patterns=[
                    "  reproduction ",
                    "( reproduction )",
                ],
            ),
        ]

    @classmethod
    def reproduction_match(cls, ent):
        return cls.from_ent(ent, reproduction=clean_trait(ent, cls.replace))


@registry.misc("reproduction_match")
def reproduction_match(ent):
    return Reproduction.reproduction_match(ent)
