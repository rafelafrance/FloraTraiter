import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const, term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

from .base import Base


@dataclass(eq=False)
class TRS(Base):
    # Class vars ----------
    trs_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "trs_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data([trs_csv], "replace")
    dir_: ClassVar[str] = """((north|east|south|west)(ing)?|[nesw])"""
    min_len: ClassVar[int] = 2
    # ---------------------

    trs: str = None
    _trs_part: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(TRSPresent=self.trs)

    @property
    def key(self):
        return "TRSPresent"

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="trs_terms", path=cls.trs_csv)
        add.trait_pipe(nlp, name="trs_part_patterns", compiler=cls.trs_part_patterns())
        add.trait_pipe(
            nlp,
            name="trs_patterns",
            overwrite=["lat_long"],
            compiler=cls.trs_patterns(),
        )
        add.cleanup_pipe(nlp, name="geocoordinate_cleanup")

    @classmethod
    def trs_part_patterns(cls):
        decoder = {
            "/": {"TEXT": {"IN": const.SLASH}},
            ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
            "99": {"LOWER": {"REGEX": r"^\d{1,2}$"}},
            "trs_post": {"LOWER": {"REGEX": r"^[nesw]$"}},
            "trs_pre": {"LOWER": {"REGEX": r"^[neswrst]{1,2}\d*$"}},
            "uaa": {"LOWER": {"REGEX": r"^u[a-z]{1,2}$"}},
            "uncert": {"ENT_TYPE": "uncertain_label"},
            "utm_dir": {"LOWER": {"REGEX": rf"""^{cls.dir_}\Z"""}},
            "utm_label": {"ENT_TYPE": "utm_label"},
        }
        return [
            Compiler(
                label="trs_part",
                keep="trs",
                decoder=decoder,
                on_match="trs_part_match",
                patterns=[
                    " trs_pre         ,?",
                    " trs_pre /? 99   ,?",
                    " trs_pre /? trs_post ,? ",
                ],
            ),
        ]

    @classmethod
    def trs_patterns(cls):
        decoder = {
            "99": {"IS_DIGIT": True},
            ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
            "sec_label": {"ENT_TYPE": "sec_label"},
            "trs_label": {"ENT_TYPE": "trs_label"},
            "trs": {"ENT_TYPE": "trs_part"},
            "not_trs": {"ENT_TYPE": "not_trs"},
        }
        return [
            Compiler(
                label="trs",
                keep="trs",
                on_match="trs_match",
                decoder=decoder,
                patterns=[
                    " trs_label* trs+",
                    " trs_label* trs+ sec_label+ 99",
                    " trs_label* trs+ sec_label+ 99 ,? 99",
                    " trs_label* sec_label+ 99 ,? trs+",
                ],
            ),
            Compiler(
                label="not_trs",
                on_match=reject_match.REJECT_MATCH,
                decoder=decoder,
                patterns=[
                    "        trs+ not_trs",
                    "not_trs trs+ not_trs",
                    "not_trs trs+",
                ],
            ),
        ]

    @classmethod
    def trs_part_match(cls, ent):
        # Enforce a minimum length
        if len(ent.text) <= cls.min_len:
            raise reject_match.RejectMatch

        trait = super().from_ent(ent, _trs_part=ent.text)

        for token in ent:
            token._.flag = "trs_part"

        ent[0]._.trait = trait
        ent[0]._.flag = "trs_data"

        return trait

    @classmethod
    def trs_match(cls, ent):
        frags = []

        for token in ent:
            if token._.flag == "trs_data":
                frags.append(token._.trait._trs_part)

            elif token._.flag == "trs_part":
                continue

            elif re.match(r"^(\d+|,)$", token.text):
                frags.append(token.text)

            elif token._.term == "sec_label":
                frags.append(token.lower_)

        trs = " ".join(frags)
        trs = re.sub(r"\s([.,:])", r"\1", trs)
        trs = re.sub(r",$", "", trs)
        if len(trs.split()) < cls.min_len:
            raise reject_match.RejectMatch

        return super().from_ent(ent, trs="present")


@registry.misc("trs_part_match")
def trs_part_match(ent):
    return TRS.trs_part_match(ent)


@registry.misc("trs_match")
def trs_match(ent):
    return TRS.trs_match(ent)
