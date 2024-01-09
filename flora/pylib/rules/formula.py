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
class Formula(Base):
    # Class vars ----------
    formula_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "formula_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data(formula_csv, "replace")
    # ---------------------

    formula: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(formula=self.formula)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="formula_terms", path=cls.formula_csv)
        add.trait_pipe(
            nlp,
            name="formula_patterns",
            compiler=cls.formula_patterns(),
            overwrite=["formula"],
        )
        add.cleanup_pipe(nlp, name="formula_cleanup")

    @classmethod
    def formula_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "formula": {"ENT_TYPE": "formula"},
        }
        return [
            Compiler(
                label="formula",
                on_match="formula_match",
                keep="formula",
                decoder=decoder,
                patterns=[
                    "  formula ",
                    "( formula )",
                ],
            ),
        ]

    @classmethod
    def formula_match(cls, ent):
        return cls.from_ent(ent, formula=clean_trait(ent, cls.replace))


@registry.misc("formula_match")
def formula_match(ent):
    return Formula.formula_match(ent)
