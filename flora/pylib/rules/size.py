from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from spacy import registry
from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.rules import terms as t_terms

from .linkable import Linkable

ALL_CSVS = [
    Path(__file__).parent / "terms" / "numeric_terms.csv",
    Path(__file__).parent / "terms" / "sex_terms.csv",
    Path(__file__).parent / "terms" / "dimension_terms.csv",
    Path(t_terms.__file__).parent / "missing_terms.csv",
    Path(t_terms.__file__).parent / "unit_distance_terms.csv",
    Path(t_terms.__file__).parent / "unit_length_terms.csv",
    Path(t_terms.__file__).parent / "unit_mass_terms.csv",
    Path(t_terms.__file__).parent / "numeric_terms.csv",
    Path(t_terms.__file__).parent / "month_terms.csv",
]


@dataclass(eq=False)
class Dimension:
    dim: str = None
    units: str = None
    min: float = None
    low: float = None
    high: float = None
    max: float = None
    uncertain: bool = None
    sex: str = None


@dataclass(eq=False)
class Size(Linkable):
    # Class vars ----------
    cross: ClassVar[list[str]] = t_const.CROSS + t_const.COMMA
    factors_cm: ClassVar[dict[str, float]] = term_util.term_data(
        ALL_CSVS,
        "factor_cm",
        float,
    )
    not_numeric: ClassVar[list[str]] = """
        not_numeric metric_mass imperial_mass metric_dist imperial_dist
        """.split()
    replace: ClassVar[dict[str, str]] = term_util.term_data(ALL_CSVS, "replace")
    lengths: ClassVar[list[str]] = ["metric_length", "imperial_length"]
    # ---------------------

    dims: list[Dimension] = field(default_factory=list)
    units: str = "cm"
    uncertain: bool = None
    # sex is in the parent class

    def to_dwc(self, dwc) -> DarwinCore:
        value = {"uncertain": self.uncertain}
        for dim in self.dims:
            value |= {
                dim.dim + "MinimumInCentimeters": dim.min,
                dim.dim + "LowInCentimeters": dim.low,
                dim.dim + "HighInCentimeters": dim.high,
                dim.dim + "MaximumInCentimeters": dim.max,
            }
        return dwc.add_dyn(**{self.key: DarwinCore.format_dict(value)})

    @property
    def key(self) -> str:
        return self.key_builder("size")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="size_terms", path=ALL_CSVS)
        add.trait_pipe(
            nlp,
            name="size_patterns",
            compiler=cls.size_patterns(),
            overwrite=["range", "dim", "sex", "metric_length", "imperial_length"],
        )

        add.cleanup_pipe(nlp, name="size_cleanup")

    @property
    def dimensions(self):
        return tuple(d.dim for d in self.dims)

    @classmethod
    def size_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "99.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
            "99-99": {"ENT_TYPE": "range"},
            ",": {"TEXT": {"IN": t_const.COMMA}},
            "about": {"ENT_TYPE": "about_term"},
            "any": {},
            "and": {"LOWER": "and"},
            "cm": {"ENT_TYPE": {"IN": cls.lengths}},
            "dim": {"ENT_TYPE": "dim"},
            "in": {"LOWER": "in"},
            "sex/dim": {"ENT_TYPE": {"IN": ["dim", "sex"]}},
            "not_numeric": {"ENT_TYPE": "not_numeric"},
            "sex": {"ENT_TYPE": "sex"},
            "sp": {"IS_SPACE": True},
            "to": {"LOWER": "to"},
            "x": {"LOWER": {"IN": t_const.CROSS + t_const.COMMA}},
        }
        return [
            Compiler(
                label="size",
                keep="size",
                on_match="size_match",
                decoder=decoder,
                patterns=[
                    "about* 99-99+ sp?                about*        cm+ in? sex/dim*",
                    "about* 99-99+ cm* sex/dim* x to? about* 99-99+ cm+ in? sex/dim*",
                    (
                        "      about* 99-99+ cm* in? sex/dim* "
                        "x to? about* 99-99+ cm* in? sex/dim* "
                        "x to? about* 99-99+ cm+ in? sex/dim*"
                    ),
                ],
            ),
            Compiler(
                label="size_high_only",
                id="size",
                on_match="size_high_only_match",
                keep="size_high_only",
                decoder=decoder,
                patterns=[
                    "to about* 99.9+ about* cm+ in? sex/dim*",
                ],
            ),
            Compiler(
                label="size_double_dim",
                id="size",
                on_match="size_double_dim_match",
                keep="size_double_dim",
                decoder=decoder,
                patterns=[
                    "about* 99-99+ cm+ sex? ,?            dim+ and dim+",
                    "about* 99-99+ cm* sex? ,? 99-99+ cm+ dim+ and dim+",
                    "about* 99-99+ cm* sex? ,? 99-99+ cm+ dim+ ,   dim+",
                ],
            ),
            Compiler(
                label="not_a_size",
                on_match=reject_match.REJECT_MATCH,
                decoder=decoder,
                patterns=[
                    "not_numeric about* 99-99+ cm+",
                    "not_numeric about* 99-99+ cm* x about* 99-99+ cm+",
                    "                   99-99+ cm not_numeric",
                ],
            ),
        ]

    @classmethod
    def scan_tokens(cls, ent):
        dims = [Dimension()]

        for token in ent:
            if token._.flag == "range_data":
                dims[-1].min = token._.trait.min
                dims[-1].low = token._.trait.low
                dims[-1].high = token._.trait.high
                dims[-1].max = token._.trait.max

            elif token._.term in ("metric_length", "imperial_length"):
                if dims[-1].units and token.lower_ in ("in",):
                    continue
                if word := cls.replace.get(token.lower_):
                    if dims[-1].units is None:
                        dims[-1].units = word
                    else:
                        dims[-1].units += word

            elif token._.term == "dim":
                if token.lower_ not in ("in",):
                    if dims[-1].dim is None:
                        dims[-1].dim = token.lower_
                    else:
                        dims[-1].dim += token.lower_
                    dims[-1].dim = cls.replace.get(dims[-1].dim, dims[-1].dim)

            elif token._.term in ("about_term", "quest"):
                dims[-1].uncertain = True

            elif token._.term == "sex":
                if word := cls.replace.get(token.lower_):
                    if dims[-1].sex is None:
                        dims[-1].sex = word
                    else:
                        dims[-1].sex += word

            elif token.lower_ in cls.cross:
                dims.append(Dimension())

        return dims

    @staticmethod
    def fill_units(dims):
        default_units = next(d.units for d in dims if d.units)

        for dim in dims:
            dim.units = dim.units if dim.units else default_units

    @staticmethod
    def fill_dimensions(dims):
        used = [d.dim for d in dims if d.dim]

        defaults = ["length", "width", "thickness"]
        defaults = [d for d in defaults if d not in used]

        for dim in dims:
            dim.dim = dim.dim if dim.dim else defaults.pop(0)

    @classmethod
    def fill_trait_data(cls, dims, ent):
        sex = next((d.sex for d in dims if d.sex), None)
        uncertain = next((d.uncertain for d in dims if d.uncertain), None)

        # Build the key and value for the range's: min, low, high, max
        for dim in dims:
            for key in ("min", "low", "high", "max"):
                value = getattr(dim, key)
                if value is None:
                    continue
                value = float(value)
                if dim.units == "m" and value > 100.0:
                    raise reject_match.RejectMatch
                if value <= 0.0:
                    raise reject_match.RejectMatch
                factor = cls.factors_cm[dim.units]
                value = round(value * factor, 3)
                setattr(dim, key, value)

            # Clear temp data
            dim.uncertain = None
            dim.units = None
            dim.sex = None

        trait = cls.from_ent(ent, dims=dims, sex=sex, uncertain=uncertain)
        return trait

    @classmethod
    def size_match(cls, ent):
        dims = cls.scan_tokens(ent)
        cls.fill_units(dims)
        cls.fill_dimensions(dims)
        return cls.fill_trait_data(dims, ent)

    @classmethod
    def size_high_only_match(cls, ent):
        dims = cls.scan_tokens(ent)
        cls.fill_units(dims)
        cls.fill_dimensions(dims)
        trait = cls.fill_trait_data(dims, ent)
        trait.dims[0].high = trait.dims[0].low
        trait.dims[0].low = None
        return trait

    @classmethod
    def size_double_dim_match(cls, ent):
        dims = cls.scan_tokens(ent)
        cls.fill_units(dims)
        cls.fill_dimensions(dims)

        trait = cls.fill_trait_data(dims, ent)

        reals = []
        for token in ent:
            if token._.term == "dim":
                reals.append(cls.replace.get(token.lower_, token.lower_))

        for real, dim in zip(reals, dims, strict=False):
            dim.dim = real

        return trait


@registry.misc("size_match")
def size_match(ent):
    return Size.size_match(ent)


@registry.misc("size_high_only_match")
def size_high_only_match(ent):
    return Size.size_high_only_match(ent)


@registry.misc("size_double_dim_match")
def size_double_dim_match(ent):
    return Size.size_double_dim_match(ent)
