from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import registry
from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib import util as t_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.rules import terms as t_terms

from .linkable import Linkable


@dataclass(eq=False)
class Count(Linkable):
    # Class vars ----------
    all_csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "count_terms.csv",
        Path(__file__).parent / "terms" / "dimension_terms.csv",
        Path(__file__).parent / "terms" / "numeric_terms.csv",
        Path(__file__).parent / "terms" / "sex_terms.csv",
        Path(t_terms.__file__).parent / "missing_terms.csv",
        Path(t_terms.__file__).parent / "unit_distance_terms.csv",
        Path(t_terms.__file__).parent / "unit_length_terms.csv",
        Path(t_terms.__file__).parent / "unit_mass_terms.csv",
        Path(t_terms.__file__).parent / "numeric_terms.csv",
        Path(t_terms.__file__).parent / "month_terms.csv",
        Path(t_terms.__file__).parent / "habitat_terms.csv",
    ]
    and_: ClassVar[list[str]] = ["&", "and", "et"]
    cross: ClassVar[list[str]] = t_const.CROSS + t_const.COMMA
    every: ClassVar[list[str]] = """ every per each or more """.split()
    not_count_prefix: ClassVar[
        list[str]
    ] = """ chapter figure fig nos no # sec sec. """.split()
    not_count_symbol: ClassVar[list[str]] = t_const.CROSS + t_const.SLASH
    replace: ClassVar[dict[str, str]] = term_util.term_data(all_csvs, "replace")
    suffix_term: ClassVar[dict[str, str]] = term_util.term_data(all_csvs, "suffix_term")
    not_numeric: ClassVar[list[str]] = """
        not_numeric metric_mass imperial_mass metric_dist imperial_dist
        """.split()
    # ---------------------

    min: int = None
    low: int = None
    high: int = None
    max: int = None
    missing: bool = None
    count_group: str = None
    per_part: str = None
    per_count: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(
            **{
                self.key: DarwinCore.format_dict(
                    {
                        "minimum": self.min,
                        "low": self.low,
                        "high": self.high,
                        "maximum": self.max,
                        "group": self.count_group,
                        "perPart": self.per_part,
                        "perCount": self.per_count,
                    },
                ),
            },
        )

    @property
    def key(self) -> str:
        return self.key_builder("count")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="count_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="count_match",
            compiler=cls.count_patterns(),
            overwrite=["range", "part", "subpart", "per_count", "habitat"],
        )
        add.cleanup_pipe(
            nlp,
            name="count_cleanup",
            delete=["range", "per_count", "num_label"],
        )

    @classmethod
    def count_patterns(cls):
        decoder = {
            "!": {"TEXT": "!"},
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "-": {"TEXT": {"IN": t_const.DASH}},
            "/": {"TEXT": {"IN": t_const.SLASH}},
            "9": {"IS_DIGIT": True},
            "99-99": {"ENT_TYPE": "range"},
            ":": {"TEXT": {"IN": t_const.COLON}},
            ";": {"TEXT": {"IN": t_const.SEMICOLON}},
            "=": {"TEXT": {"IN": ["=", ":"]}},
            "[.,]": {"LOWER": {"IN": t_const.COMMA + t_const.DOT}},
            "adp": {"POS": "ADP"},
            "any": {},
            "as": {"LOWER": {"IN": ["as"]}},
            "count_suffix": {"ENT_TYPE": "count_suffix"},
            "count_word": {"ENT_TYPE": {"IN": ["count_word", "number_word"]}},
            "dim": {"ENT_TYPE": "dim"},
            "every": {"LOWER": {"IN": cls.every}},
            "habitat": {"ENT_TYPE": "habitat"},
            "is_alpha": {"IS_ALPHA": True},
            "missing": {"ENT_TYPE": "missing"},
            "not_count_symbol": {"LOWER": {"IN": cls.not_count_symbol}},
            "not_numeric": {"ENT_TYPE": {"IN": cls.not_numeric}},
            "or": {"POS": {"IN": ["CONJ"]}},
            "part": {"ENT_TYPE": {"IN": ["part", "subpart"]}},
            "per_count": {"ENT_TYPE": "per_count"},
            "subpart": {"ENT_TYPE": "subpart"},
            "X": {"LOWER": "x"},
            "x": {"LOWER": {"IN": t_const.CROSS + t_const.COMMA}},
            "°": {"TEXT": "°"},
        }
        return [
            Compiler(
                label="count",
                on_match="count_match",
                decoder=decoder,
                keep="count",
                patterns=[
                    "  99-99+",
                    "( 99-99+ )  every+ part",
                    "missing? 99-99+ count_suffix+",
                    "count_word      count_suffix+",
                    "missing? 99-99+ subpart+",
                    "count_word      subpart+",
                    " per_count+ adp? 99-99+",
                    "  99-99+ -*             per_count+",
                    "( 99-99+ )              per_count+",
                    "  99-99+ -* every+ part per_count*",
                    "99-99+ per_count+ adp? 99-99+",
                ],
            ),
            Compiler(
                label="count_word",
                id="count",
                keep="count",
                on_match="count_word_match",
                decoder=decoder,
                patterns=[
                    "count_word",
                ],
            ),
            Compiler(
                label="not_a_count",
                on_match=reject_match.REJECT_MATCH,
                decoder=decoder,
                patterns=[
                    "not_numeric [.,]? 99-99+",
                    "9 / 9",
                    "X =? 99-99+",
                    "99-99+ ; 99-99+",
                    "99-99+ x 99-99+",
                    "99-99+ :",
                    "99-99+ any? any? any? as dim",
                    "99-99+ °",
                    "! -? 9",
                    "is_alpha - 9",
                    "9 not_numeric",
                    "habitat+ 99-99+",
                ],
            ),
        ]

    @classmethod
    def count_match(cls, ent):
        per_part = []
        suffix = []
        kwargs = {}

        for token in ent:
            if token._.flag == "range_data":
                for key in ("min", "low", "high", "max"):
                    if value := getattr(token._.trait, key, None):
                        value = t_util.to_positive_int(value)
                        if value is None:
                            raise reject_match.RejectMatch
                        kwargs[key] = value

            elif token._.term == "number_word":
                value = cls.replace.get(token.lower_, token.lower_)
                kwargs["low"] = t_util.to_positive_int(value)

            elif token.ent_type_ in ("count_suffix", "subpart"):
                suffix.append(token.lower_)

            elif token._.trait and token._.flag == "part":
                part_trait = token._.trait.trait
                kwargs["per_part"] = getattr(token._.trait, part_trait)

            elif token._.term == "per_count":
                per_part.append(token.lower_)

            elif token._.term == "missing":
                kwargs["missing"] = True

        if per_part:
            per_part = " ".join(per_part)
            kwargs["count_group"] = cls.replace.get(per_part, per_part)

        if suffix:
            suffix = "".join(suffix)
            value = cls.replace.get(suffix, suffix)
            key = cls.suffix_term.get(suffix)
            if key:
                kwargs[key] = value

        return cls.from_ent(ent, **kwargs)

    @classmethod
    def count_word_match(cls, ent):
        return cls.from_ent(ent, low=int(cls.replace[ent[0].lower_]))


@registry.misc("count_match")
def count_match(ent):
    return Count.count_match(ent)


@registry.misc("count_word_match")
def count_word_match(ent):
    return Count.count_word_match(ent)
