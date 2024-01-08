from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry

from traiter.pylib.darwin_core import DarwinCore
from traiter.traiter.pylib import term_util
from traiter.traiter.pylib.pattern_compiler import Compiler
from traiter.traiter.pylib.pipes import add
from traiter.traiter.pylib.pipes.reject_match import REJECT_MATCH

from .base import Base


@dataclass(eq=False)
class Habitat(Base):
    # Class vars ----------
    habitat_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "habitat_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data(habitat_csv, "replace")
    sep: ClassVar[str] = "/,-"
    # ---------------------

    habitat: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(habitat=self.habitat)

    @property
    def key(self):
        return DarwinCore.ns("habitat")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="habitat_terms", path=cls.habitat_csv)
        add.trait_pipe(nlp, name="habitat_patterns", compiler=cls.habitat_compilers())
        add.cleanup_pipe(nlp, name="habitat_cleanup")

    @classmethod
    def habitat_compilers(cls):
        decoder = {
            "bad": {"ENT_TYPE": "bad_habitat"},
            "not_eol": {"LOWER": {"REGEX": r"^[^;.]+$"}},
            "habitat": {"ENT_TYPE": "habitat_term"},
            "label": {"ENT_TYPE": "habitat_label"},
            "prefix": {"ENT_TYPE": "habitat_prefix"},
            "sep": {"LOWER": {"REGEX": rf"[{cls.sep}]"}},
            "suffix": {"ENT_TYPE": "habitat_suffix"},
        }

        return [
            Compiler(
                label="habitat",
                on_match="habitat_match",
                decoder=decoder,
                keep="habitat",
                patterns=[
                    "        habitat+",
                    "prefix+ sep? prefix* habitat+",
                    "prefix+ sep? prefix* habitat+ sep? suffix+",
                    "        sep? prefix* habitat+ sep? suffix+",
                    "prefix+ sep? prefix*          sep? suffix+",
                ],
            ),
            Compiler(
                label="labeled_habitat",
                id="habitat",
                on_match="labeled_habitat",
                decoder=decoder,
                keep="habitat",
                patterns=[
                    "label+ not_eol+",
                ],
            ),
            Compiler(
                label="not_habitat",
                decoder=decoder,
                on_match=REJECT_MATCH,
                patterns=[
                    "bad habitat+",
                    "bad habitat+ bad",
                    "    habitat+ bad",
                ],
            ),
        ]

    @classmethod
    def habitat_match(cls, ent):
        frags = []

        for token in ent:
            if token.text not in cls.sep:
                frags.append(cls.replace.get(token.lower_, token.lower_))

        habitat = " ".join(frags)

        return super().from_ent(ent, habitat=habitat)

    @classmethod
    def labeled_match(cls, ent):
        i = 0
        for i, token in enumerate(ent):
            if token._.term != "habitat_label":
                break
        habitat = " ".join(ent[i:].text.split())
        trait = super().from_ent(ent, habitat=habitat)
        trait.trait = "habitat"
        return trait


@registry.misc("habitat_match")
def habitat_match(ent):
    return Habitat.habitat_match(ent)


@registry.misc("labeled_habitat")
def labeled_habitat(ent):
    return Habitat.labeled_match(ent)
