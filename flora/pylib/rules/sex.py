from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy import registry

import traiter.traiter.pylib.darwin_core as t_dwc
from traiter.traiter.pylib import const as t_const
from traiter.traiter.pylib import term_util
from traiter.traiter.pylib.darwin_core import DarwinCore
from traiter.traiter.pylib.pattern_compiler import Compiler
from traiter.traiter.pylib.pipes import add
from traiter.traiter.pylib.rules.base import Base

from ..trait_util import clean_trait


@dataclass(eq=False)
class Sex(Base):
    # Class vars ----------
    sex_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "sex_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data(sex_csv, "replace")
    # ---------------------

    sex: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(sex=self.sex)

    @property
    def key(self) -> str:
        return t_dwc.DarwinCore.ns("sex")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="sex_terms", path=cls.sex_csv)
        add.trait_pipe(
            nlp,
            name="sex_patterns",
            compiler=cls.sex_patterns(),
            overwrite=["sex"],
        )
        add.cleanup_pipe(nlp, name="sex_cleanup")

    @classmethod
    def sex_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "sex": {"ENT_TYPE": "sex"},
        }
        return [
            Compiler(
                label="sex",
                on_match="sex_match",
                keep="sex",
                decoder=decoder,
                patterns=[
                    "  sex ",
                    "( sex )",
                ],
            ),
        ]

    @classmethod
    def sex_match(cls, ent):
        return cls.from_ent(ent, sex=clean_trait(ent, cls.replace))


@registry.misc("sex_match")
def sex_match(ent):
    return Sex.sex_match(ent)
