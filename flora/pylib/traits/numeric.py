import re
from dataclasses import dataclass
from pathlib import Path

from spacy import registry
from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib import pattern_compiler as comp
from traiter.pylib import term_util
from traiter.pylib import util as t_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes import reject_match
from traiter.pylib.traits import terms as t_terms

from .part import PART_LABELS

ALL_CSVS = [
    Path(__file__).parent / "terms" / "numeric_terms.csv",
    Path(__file__).parent / "terms" / "missing_terms.csv",
    Path(__file__).parent / "terms" / "sex_terms.csv",
    Path(t_terms.__file__).parent / "unit_distance_terms.csv",
    Path(t_terms.__file__).parent / "unit_length_terms.csv",
    Path(t_terms.__file__).parent / "unit_mass_terms.csv",
    Path(t_terms.__file__).parent / "numeric_terms.csv",
    Path(t_terms.__file__).parent / "month_terms.csv",
]

ALL_PARTS = PART_LABELS + ["subpart"]
AND = ["&", "and", "et"]
CONJ = AND + ["or"]
CROSS = t_const.CROSS + t_const.COMMA
EVERY = """ every per each or more """.split()
FACTORS_CM = term_util.term_data(ALL_CSVS, "factor_cm", float)
MIN_OR = t_const.FLOAT_RE + f"(or|{'|'.join(AND)})"
NOT_COUNT_PREFIX = """ chapter figure fig nos no # sec sec. """.split()
NOT_COUNT_SYMBOL = t_const.CROSS + t_const.SLASH
NOT_NUMERIC = """
    not_numeric metric_mass imperial_mass metric_dist imperial_dist
    """.split()
REPLACE = term_util.term_data(ALL_CSVS, "replace")
SUFFIX_TERM = term_util.term_data(ALL_CSVS, "suffix_term")
TO = ["to"]


@dataclass()
class Dimension:
    range: dict
    units: str
    dim: str
    about: bool
    sex: str


def build(nlp: Language):
    add.term_pipe(nlp, name="numeric_terms", path=ALL_CSVS)
    add.trait_pipe(
        nlp,
        name="range_patterns",
        compiler=range_patterns(),
    )
    add.trait_pipe(
        nlp,
        name="numeric_patterns",
        compiler=count_patterns() + size_patterns(),
        overwrite=[*ALL_PARTS, "sex"],
    )
    # add.debug_tokens(nlp)  # #########################################
    comp.ACCUMULATOR.delete(NOT_NUMERIC)
    add.cleanup_pipe(nlp, name="numeric_cleanup")


def range_patterns():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        ",": {"TEXT": {"IN": t_const.COMMA}},
        "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
        "-/or": {"LOWER": {"IN": t_const.DASH + TO + CONJ + ["_"]}, "OP": "+"},
        "-/to": {"LOWER": {"IN": t_const.DASH + TO + ["_"]}, "OP": "+"},
        "9": {"IS_DIGIT": True},
        "9.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
        "[+]": {"TEXT": {"IN": t_const.PLUS}},
        "[?]": {"TEXT": {"IN": t_const.Q_MARK}},
        "a.": {"LOWER": {"REGEX": r"^[a-ln-wyz]\.?$"}},  # Keep meters and a cross
        "ambiguous": {"LOWER": {"IN": ["few", "many"]}},
        "and/or": {"LOWER": {"IN": CONJ}},
        "bad_follower": {"LOWER": {"REGEX": r"^[=:]$"}},
        "bad_leader": {"LOWER": {"REGEX": r"^[=]$"}},
        "bad_symbol": {"TEXT": {"REGEX": r"^[&/°'\"]+$"}},
        "conj": {"POS": {"IN": ["CCONJ"]}},
        "9.9or": {"LOWER": {"REGEX": MIN_OR}},
        "month": {"ENT_TYPE": "month"},
        "not_numeric": {"ENT_TYPE": {"IN": NOT_NUMERIC}},
    }

    return [
        Compiler(
            label="range.low",
            id="range",
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


def count_patterns():
    decoder = {
        "!": {"TEXT": "!"},
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        "-": {"TEXT": {"IN": t_const.DASH}},
        "/": {"TEXT": {"IN": t_const.SLASH}},
        "9": {"IS_DIGIT": True},
        "99-99": {"ENT_TYPE": "range", "OP": "+"},
        ":": {"TEXT": {"IN": t_const.COLON}},
        ";": {"TEXT": {"IN": t_const.SEMICOLON}},
        "=": {"TEXT": {"IN": ["=", ":"]}},
        "[.,]": {"LOWER": {"IN": t_const.COMMA + t_const.DOT}},
        "adp": {"POS": {"IN": ["ADP"]}},
        "any": {},
        "as": {"LOWER": {"IN": ["as"]}},
        "count_suffix": {"ENT_TYPE": "count_suffix"},
        "count_word": {"ENT_TYPE": {"IN": ["count_word", "number_word"]}},
        "dim": {"ENT_TYPE": "dim"},
        "every": {"LOWER": {"IN": EVERY}},
        "is_alpha": {"IS_ALPHA": True},
        "missing": {"ENT_TYPE": "missing"},
        "not_count_symbol": {"LOWER": {"IN": NOT_COUNT_SYMBOL}},
        "not_numeric": {"ENT_TYPE": {"IN": NOT_NUMERIC}},
        "part": {"ENT_TYPE": {"IN": ALL_PARTS}},
        "per_count": {"ENT_TYPE": "per_count"},
        "subpart": {"ENT_TYPE": "subpart"},
        "X": {"LOWER": "x"},
        "x": {"LOWER": {"IN": t_const.CROSS + t_const.COMMA}},
        "°": {"TEXT": "°"},
    }

    return [
        Compiler(
            label="count",
            id="count",
            on_match="count_match",
            decoder=decoder,
            keep="count",
            patterns=[
                "  99-99",
                "  99-99 -*             per_count+",
                "( 99-99 )              per_count+",
                "  99-99 -* every+ part per_count*",
                "( 99-99 )  every+ part",
                "per_count+ adp? 99-99",
                "missing? 99-99 count_suffix+",
                "count_word     count_suffix+",
                "missing? 99-99 subpart+",
                "count_word     subpart+",
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
                "not_numeric [.,]? 99-99",
                "9 / 9",
                "X =? 99-99",
                "99-99 ; 99-99",
                "99-99 x 99-99",
                "99-99 :",
                "99-99 any? any? any? as dim",
                "99-99 °",
                "! -? 9",
                "is_alpha - 9",
                "9  not_numeric",
            ],
        ),
    ]


def size_patterns():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
        "99-99": {"ENT_TYPE": "range", "OP": "+"},
        ",": {"TEXT": {"IN": t_const.COMMA}},
        "about": {"ENT_TYPE": "about"},
        "any": {},
        "and": {"LOWER": "and"},
        "cm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
        "dim": {"ENT_TYPE": "dim"},
        "in": {"LOWER": "in"},
        "sex/dim": {"ENT_TYPE": {"IN": ["dim", "sex"]}},
        "not_numeric": {"ENT_TYPE": "not_numeric"},
        "sex": {"ENT_TYPE": "sex"},
        "to": {"LOWER": "to"},
        "x": {"LOWER": {"IN": t_const.CROSS + t_const.COMMA}},
    }

    return [
        Compiler(
            label="size",
            id="size",
            on_match="size_match",
            keep="size",
            decoder=decoder,
            patterns=[
                "about* 99-99                    about*       cm+ in? sex/dim*",
                "about* 99-99                    about*       cm+ in? sex/dim*",
                "about* 99-99 cm* sex/dim* x to? about* 99-99 cm+ in? sex/dim*",
                (
                    "      about* 99-99 cm* in? sex/dim* "
                    "x to? about* 99-99 cm* in? sex/dim* "
                    "x to? about* 99-99 cm+ in? sex/dim*"
                ),
            ],
        ),
        Compiler(
            label="size.high_only",
            id="size",
            on_match="size_high_only_match",
            keep="size",
            decoder=decoder,
            patterns=[
                "to about* 99.9 about* cm+ in? sex/dim*",
            ],
        ),
        Compiler(
            label="size.double_dim",
            id="size",
            on_match="size_double_dim_match",
            keep="size",
            decoder=decoder,
            patterns=[
                "about* 99-99 cm+ sex? ,? dim+ and  dim+",
                "about* 99-99 cm* sex? ,? 99-99 cm+ dim+ and dim+",
                "about* 99-99 cm* sex? ,? 99-99 cm+ dim+ ,   dim+",
            ],
        ),
        Compiler(
            label="not_a_size",
            on_match=reject_match.REJECT_MATCH,
            decoder=decoder,
            patterns=[
                "not_numeric about* 99-99 cm+",
                "not_numeric about* 99-99 cm* x about* 99-99 cm+",
                "                   99-99 cm not_numeric",
            ],
        ),
    ]


@registry.misc("range_match")
def range_match(ent):
    nums = []
    for token in ent:

        if token._.term == "per_count":
            raise reject_match.RejectMatch

        token._.flag = "range"
        nums += re.findall(r"\d*\.?\d+", token.text)

    # Cache the values in the first token
    keys = ent.label_.split(".")[1:]
    ent[0]._.data = {k: v for k, v in zip(keys, nums)}
    ent[0]._.flag = "range_data"


@registry.misc("count_match")
def count_match(ent):
    per_part = []
    suffix = []
    data = {}

    for token in ent:

        if token._.flag == "range_data":
            for key, value in token._.data.items():
                value = t_util.to_positive_int(value)
                if value is None:
                    raise reject_match.RejectMatch
                data[key] = value

        elif token._.term == "number_word":
            value = REPLACE.get(token.lower_, token.lower_)
            data["low"] = t_util.to_positive_int(value)

        elif token._.data and token._.term == "subpart":
            subpart = token._.data["subpart"]
            data["subpart"] = subpart

        elif token._.term in ("count_suffix", "subpart"):
            suffix.append(token.lower_)

        elif token._.data and token._.flag == "part":
            part_trait = token._.data["trait"]
            data["per_part"] = token._.data[part_trait]

        elif token._.term == "per_count":
            per_part.append(token.lower_)

        elif token._.term == "missing":
            data["missing"] = True

    if per_part:
        per_part = " ".join(per_part)
        data["count_group"] = REPLACE.get(per_part, per_part)

    if suffix:
        suffix = "".join(suffix)
        value = REPLACE.get(suffix, suffix)
        key = SUFFIX_TERM.get(suffix)
        if key:
            data[key] = value

    ent._.data = data


@registry.misc("count_word_match")
def count_word_match(ent):
    ent._.data = {"low": int(REPLACE[ent[0].lower_])}


@registry.misc("size_match")
def size_match(ent):
    dimensions = scan_tokens(ent)
    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)


@registry.misc("size_high_only_match")
def size_high_only_match(ent):
    dimensions = scan_tokens(ent)
    dimensions[0].range = {"high": dimensions[0].range["low"]}
    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)


@registry.misc("size_double_dim_match")
def size_double_dim_match(ent):
    dimensions = scan_tokens(ent)

    dims = []
    for token in ent:
        if token._.term == "dim":
            dims.append(REPLACE.get(token.lower_, token.lower_))

    for dimension, dim in zip(dimensions, dims):
        dimension.dim = dim

    fill_units(dimensions)
    fill_dimensions(dimensions)
    fill_trait_data(dimensions, ent)


def scan_tokens(ent):
    dimensions = [Dimension(range={}, units="", dim="", about=False, sex="")]

    for token in ent:

        if token._.flag == "range_data":
            dimensions[-1].range = token._.data

        elif token._.term in ("metric_length", "imperial_length"):
            if dimensions[-1].units and token.lower_ in ("in",):
                continue
            if word := REPLACE.get(token.lower_):
                dimensions[-1].units += word

        elif token._.term == "dim":
            if token.lower_ not in ("in",):
                dimensions[-1].dim += token.lower_
                dimensions[-1].dim = REPLACE.get(dimensions[-1].dim, dimensions[-1].dim)

        elif token._.term in ("about", "quest"):
            dimensions[-1].about = True

        elif token._.term == "sex":
            if word := REPLACE.get(token.lower_):
                dimensions[-1].sex += word

        elif token.lower_ in CROSS:
            new = Dimension(range={}, units="", dim="", about=False, sex="")
            dimensions.append(new)

    return dimensions


def fill_units(dimensions):
    default_units = next(d.units for d in dimensions if d.units)

    for dim in dimensions:
        dim.units = dim.units if dim.units else default_units


def fill_dimensions(dimensions):
    used = [d.dim for d in dimensions if d.dim]

    defaults = ["length", "width", "thickness"]
    defaults = [d for d in defaults if d not in used]

    for dim in dimensions:
        dim.dim = dim.dim if dim.dim else defaults.pop(0)


def fill_trait_data(dimensions, ent):
    data = {"units": "cm"}

    if sex := [d.sex for d in dimensions if d.sex]:
        data["sex"] = sex[0]

    if any(d.about for d in dimensions):
        data["uncertain"] = True

    # "dimensions" is used to link traits
    dims = sorted(d.dim for d in dimensions)
    data["dimensions"] = dims if len(dims) > 1 else dims[0]

    # Build the key and value for the range's: min, low, high, max
    for dim in dimensions:
        for key, value in dim.range.items():
            key = f"{dim.dim}_{key}"
            factor = FACTORS_CM[dim.units]
            value = t_util.to_positive_float(value)
            if dim.units == "m" and value > 100.0:
                raise reject_match.RejectMatch
            value = round(value * factor, 3)
            data[key] = value

    ent._.data = data
