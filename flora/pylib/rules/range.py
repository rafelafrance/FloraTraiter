import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.rules import terms as t_terms

from .linkable import Linkable


@dataclass(eq=False)
class Range(Linkable):
    # Class vars ----------
    all_csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "about_terms.csv",
        Path(t_terms.__file__).parent / "numeric_terms.csv",
        Path(t_terms.__file__).parent / "month_terms.csv",
    ]

    and_: ClassVar[list[str]] = ["&", "and", "et"]
    conj: ClassVar[list[str]] = [*and_, "or"]
    min_or: ClassVar[list[str]] = t_const.FLOAT_RE + f"(or|{'|'.join(and_)})"
    not_count_symbol: ClassVar[list[str]] = t_const.CROSS + t_const.SLASH
    not_numeric: ClassVar[list[str]] = """
        not_numeric metric_mass imperial_mass metric_dist imperial_dist
        """.split()
    to: ClassVar[list[str]] = ["to"]
    # ---------------------

    min: float = None
    low: float = None
    high: float = None
    max: float = None

    def to_dwc(self, dwc) -> DarwinCore:
        key = self.key
        return dwc.add_dyn(
            **{
                key + "Minimum": self.min,
                key + "Low": self.low,
                key + "High": self.high,
                key + "Maximum": self.max,
            },
        )

    @property
    def key(self) -> str:
        return self.key_builder("range")

    @classmethod
    def pipe(cls, nlp: Language, overwrite=None):
        overwrite = overwrite if overwrite else []
        add.term_pipe(nlp, name="range_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="range_patterns",
            overwrite=overwrite,
            compiler=cls.range_patterns(),
        )
        # Keep these traits around for building size and count traits

    @classmethod
    def range_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            ",": {"TEXT": {"IN": t_const.COMMA}},
            "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
            "-/or": {
                "LOWER": {"IN": t_const.DASH + cls.to + cls.conj + ["_"]},
                "OP": "+",
            },
            "-/to": {"LOWER": {"IN": t_const.DASH + cls.to + ["_"]}, "OP": "+"},
            "9": {"IS_DIGIT": True},
            "9.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
            "[+]": {"TEXT": {"IN": t_const.PLUS}},
            "[?]": {"TEXT": {"IN": t_const.Q_MARK}},
            "a.": {"LOWER": {"REGEX": r"^[a-ln-wyz]\.?$"}},
            "ambiguous": {"LOWER": {"IN": ["few", "many"]}},
            "and/or": {"LOWER": {"IN": cls.conj}},
            "bad_follower": {"LOWER": {"REGEX": r"^[=:]$"}},
            "bad_leader": {"LOWER": {"REGEX": r"^[=]$"}},
            "bad_symbol": {"TEXT": {"REGEX": r"^[&/°'\"]+$"}},
            "conj": {"POS": {"IN": ["CCONJ"]}},
            "9.9or": {"LOWER": {"REGEX": cls.min_or}},
            "month": {"ENT_TYPE": "month"},
            "not_numeric": {"ENT_TYPE": {"IN": cls.not_numeric}},
        }
        return [
            Compiler(
                label="range.low",
                id="range",
                keep="range",
                on_match="range_match",
                decoder=decoder,
                patterns=[
                    "9.9",
                    "( 9.9 -/or ) ambiguous ( -/to ambiguous )",
                    "9.9 ( -/to [?] )",
                ],
            ),
            Compiler(
                label="range.min.low",
                id="range",
                keep="range",
                on_match="range_match",
                decoder=decoder,
                patterns=[
                    "( 9.9 -/or ) 9.9",
                    "( 9.9 -/to ) 9.9",
                    "( 9.9or ) 9.9",
                ],
            ),
            Compiler(
                label="range.low.high",
                id="range",
                keep="range",
                on_match="range_match",
                decoder=decoder,
                patterns=[
                    "9.9 and/or 9.9",
                    "9.9 -/to   9.9",
                    "9 -* conj 9",
                ],
            ),
            Compiler(
                label="range.low.max",
                id="range",
                keep="range",
                on_match="range_match",
                decoder=decoder,
                patterns=[
                    "9.9 ( and/or 9.9 )",
                    "9.9 ( -/to   9.9 )",
                ],
            ),
            Compiler(
                label="range.min.low.high",
                id="range",
                keep="range",
                on_match="range_match",
                decoder=decoder,
                patterns=[
                    "( 9.9   -/or )   9.9 -/to     9.9",
                    "( 9.9   -/or )   9.9 - and/or 9.9",
                    "( 9.9   and/or ) 9.9   and/or 9.9",
                    "  9.9 ( and/or   9.9    -/to  9.9 )",
                    "( 9.9or )        9.9 -/to     9.9",
                    "( 9.9or )        9.9 - and/or 9.9",
                ],
            ),
            Compiler(
                label="range.min.low.max",
                id="range",
                keep="range",
                on_match="range_match",
                decoder=decoder,
                patterns=[
                    "( 9.9 - ) 9.9 -? ( -/to 9.9 [+]? )",
                    "( 9.9or ) 9.9 -? ( -/to 9.9 [+]? )",
                    "  9.9 -   9.9 - ( -/to 9.9 )",
                    "  9.9 - and/or 9.9 -/to 9.9",
                ],
            ),
            Compiler(
                label="range.low.high.max",
                id="range",
                keep="range",
                on_match="range_match",
                decoder=decoder,
                patterns=[
                    "9.9 ( and/or 9.9 -/or 9.9 [+]? )",
                    "9.9 - 9.9   ( -/to 9.9 [+]? )",
                    "9.9 - 9.9 - ( -/to 9.9 [+]? )",
                    "9.9 - 9.9 - 9.9",
                    "9.9 -/to 9.9 and/or 9.9",
                    "9.9 - and/or 9.9 ( -/or 9.9 [+]? )",
                    "9.9 and/or 9.9 ( and/or 9.9 [+]? )",
                ],
            ),
            Compiler(
                label="range.min.low.high.max",
                id="range",
                keep="range",
                on_match="range_match",
                decoder=decoder,
                patterns=[
                    "( 9.9 - ) 9.9 - 9.9 ( -/to 9.9 [+]? )",
                    "( 9.9 -/or ) 9.9 - and/or 9.9 ( -/or 9.9 [+]? )",
                    "( 9.9 and/or ) 9.9 - and/or 9.9 ( and/or 9.9 [+]? )",
                    "9.9 - and/or 9.9 - and/or 9.9 -/to 9.9",
                    "9.9 - and/or 9.9 -/to 9.9 ( -/or 9.9 [+]? )",
                    "9.9 -/to 9.9 ( -/or 9.9 ) ( -/or 9.9 [+]? )",
                    "9.9 9.9 -/to and/or 9.9 ( -/or 9.9 [+]? )",
                    "9.9 and/or 9.9 - 9.9 ( -/or 9.9 [+]? )",
                    "( 9.9or ) 9.9 - 9.9 ( -/to 9.9 [+]? )",
                    "( 9.9or ) 9.9 - and/or 9.9 ( -/or 9.9 [+]? )",
                ],
            ),
            Compiler(
                label="not_a_range",
                on_match=reject_match.REJECT_MATCH,
                decoder=decoder,
                patterns=[
                    "9.9 bad_symbol",
                    "    bad_symbol 9.9",
                    "9.9 bad_symbol 9.9",
                    "    bad_symbol 9.9 - 9.9",
                    "9.9 month",
                    "    month 9.9",
                    "9.9 not_numeric",
                    "    not_numeric     ,? 9.9",
                    "    not_numeric 9.9 ,  9.9",
                    "9   a.",
                    "    bad_leader  9.9",
                    "9.9 bad_follower",
                ],
            ),
        ]

    @classmethod
    def range_match(cls, ent):
        nums = []
        for token in ent:
            if token._.term == "per_count":
                raise reject_match.RejectMatch

            token._.flag = "range"
            nums += re.findall(r"\d*\.?\d+", token.text)

        keys = ent.label_.split(".")[1:]
        kwargs = dict(zip(keys, nums, strict=False))

        trait = cls.from_ent(ent, **kwargs)

        # Cache the values in the first token
        ent[0]._.trait = trait
        ent[0]._.flag = "range_data"

        return trait


@registry.misc("range_match")
def range_match(ent):
    return Range.range_match(ent)
