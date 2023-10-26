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
class Venation(Linkable):
    # Class vars ----------
    venation_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "venation_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(venation_csv, "replace")
    # ---------------------

    venation: str = None

    def to_dwc(self, dwc, ent):
        key = self.dwc_key("venation")
        dwc.add_dyn(**{key: self.venation})
        self.add_loc(dwc, "venation")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="venation_terms", path=cls.venation_csv)
        add.trait_pipe(
            nlp,
            name="venation_patterns",
            compiler=cls.venation_patterns(),
            overwrite=["venation"],
        )
        add.cleanup_pipe(nlp, name="venation_cleanup")

    @classmethod
    def venation_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "venation": {"ENT_TYPE": "venation"},
        }
        return [
            Compiler(
                label="venation",
                on_match="venation_match",
                keep="venation",
                decoder=decoder,
                patterns=[
                    "  venation ",
                    "( venation )",
                ],
            ),
        ]

    @classmethod
    def venation_match(cls, ent):
        return cls.from_ent(ent, venation=clean_trait(ent, cls.replace))


@registry.misc("venation_match")
def venation_match(ent):
    return Venation.venation_match(ent)
