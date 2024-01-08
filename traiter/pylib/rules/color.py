from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const, term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from .base import Base


@dataclass(eq=False)
class Color(Base):
    # Class vars ----------
    color_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "color_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data(color_csv, "replace")
    remove: ClassVar[dict[str, int]] = term_util.term_data(color_csv, "remove", int)
    # ---------------------

    color: str = None
    missing: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.color})

    @property
    def key(self):
        return "missingColor" if self.missing else "color"

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="color_terms", path=cls.color_csv)
        add.trait_pipe(nlp, name="color_patterns", compiler=cls.color_patterns())
        add.cleanup_pipe(nlp, name="color_cleanup")

    @classmethod
    def color_patterns(cls):
        return [
            Compiler(
                label="color",
                on_match="color_match",
                keep="color",
                decoder={
                    "-": {"TEXT": {"IN": const.DASH}},
                    "color": {"ENT_TYPE": "color_term"},
                    "color_words": {"ENT_TYPE": {"IN": ["color_term", "color_mod"]}},
                    "missing": {"ENT_TYPE": "color_missing"},
                    "to": {"POS": {"IN": ["AUX"]}},
                },
                patterns=[
                    "missing? color_words* -* color+ -* color_words*",
                    "missing? color_words+ to color_words+ color+ -* color_words*",
                ],
            ),
        ]

    @classmethod
    def color_match(cls, ent):
        missing = None
        frags = []
        for token in ent:
            # Skip anything that is not a term or is flagged for removal
            if (
                not token._.term
                or cls.remove.get(token.lower_)
                or token.text in const.DASH
            ):
                continue

            # Color is noted as missing
            if token._.term == "color_missing":
                missing = True
                continue

            frag = cls.replace.get(token.lower_, token.lower_)

            # Skip duplicate colors within the entity
            if frag not in frags:
                frags.append(frag)

        # Build the color
        value = "-".join(frags)
        color = cls.replace.get(value, value)

        return super().from_ent(ent, color=color, missing=missing)


@registry.misc("color_match")
def color_match(ent):
    return Color.color_match(ent)
