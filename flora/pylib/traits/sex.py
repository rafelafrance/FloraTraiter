from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits.base import Base

from flora.pylib.darwin_core import DarwinCore

from ..trait_util import clean_trait


@dataclass(eq=False)
class Sex(Base):
    # Class vars ----------
    sex_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "sex_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data(sex_csv, "replace")
    # ---------------------

    sex: str = None

    def to_dwc(self, dwc) -> None:
        dwc.add(sex=self.sex)

    @property
    def key(self):
        return DarwinCore.ns("sex")

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
