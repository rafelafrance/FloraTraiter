import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const, term_util, util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from .base import Base


@dataclass(eq=False)
class Elevation(Base):
    # Class vars ----------
    float_re: ClassVar[str] = r"^(\d[\d,.]+)\Z"
    all_units: ClassVar[list[str]] = ["metric_length", "imperial_length"]
    elevation_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "elevation_terms.csv"
    )
    unit_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "unit_length_terms.csv"
    about_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "about_terms.csv"
    tic_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "unit_tic_terms.csv"
    all_csvs: ClassVar[list[Path]] = [elevation_csv, unit_csv, about_csv, tic_csv]

    replace: ClassVar[dict[str, str]] = term_util.term_data(all_csvs, "replace")
    factors_cm: ClassVar[dict[str, float]] = term_util.term_data(
        (unit_csv, tic_csv),
        "factor_cm",
        float,
    )
    factors_m: ClassVar[dict[str, float]] = {
        k: v / 100.0 for k, v in factors_cm.items()
    }
    # ---------------------

    elevation: float = None
    elevation_high: float = None
    units: str = None
    about: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        dwc.add(
            verbatimElevation=self._text,
            minimumElevationInMeters=self.elevation,
            maximumElevationInMeters=self.elevation_high,
        )
        about = "uncertain" if self.about else None
        return dwc.add_dyn(elevationUncertain=about)

    @property
    def key(self):
        return DarwinCore.ns("elevation")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="elevation_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="elevation_patterns",
            compiler=cls.elevation_compilers(),
        )
        add.cleanup_pipe(nlp, name="elevation_cleanup")

    @classmethod
    def elevation_compilers(cls):
        label_ender = r"[:=;,.]"
        return [
            Compiler(
                label="elevation",
                on_match="elevation_match",
                keep="elevation",
                decoder={
                    "(": {"TEXT": {"IN": const.OPEN}},
                    ")": {"TEXT": {"IN": const.CLOSE}},
                    "-/to": {"LOWER": {"IN": [*const.DASH, "to", "_"]}, "OP": "+"},
                    "/": {"TEXT": {"IN": const.SLASH}},
                    "99": {"TEXT": {"REGEX": cls.float_re}},
                    ":": {"TEXT": {"REGEX": rf"^{label_ender}+\Z"}},
                    ",": {"TEXT": {"REGEX": rf"^{label_ender}+\Z"}},
                    "about": {"ENT_TYPE": "about_term"},
                    "label": {"ENT_TYPE": "elev_label"},
                    "m": {"ENT_TYPE": {"IN": cls.all_units}},
                    "sp": {"IS_SPACE": True},
                },
                patterns=[
                    "label+ :? sp? about? ,? 99 sp? m",
                    "label+ :? sp? about? ,? 99 sp? m sp? ( 99 m ,? )",
                    "label+ :? sp? about? ,? 99 sp? m sp? / 99 m",
                    "              about? ,? 99 sp? m sp? ( 99 m ,? )",
                    "              about? ,? 99 sp? m sp? / 99 m",
                    "label+ :? sp? about? ,? 99 sp? -/to sp? 99 sp? m",
                ],
            ),
        ]

    @classmethod
    def elevation_match(cls, ent):
        values = []
        units_ = ""
        expected_len = 1
        about = None
        hi = None

        for token in ent:
            # Find numbers
            if re.match(const.FLOAT_RE, token.text) and len(values) < expected_len:
                values.append(util.to_positive_float(token.text))

            # Find units
            elif token._.term in cls.all_units and not units_:
                units_ = cls.replace.get(token.lower_, token.lower_)

            elif token._.term == "about_term":
                about = True

            # If there's a dash it's a range
            elif token.lower_ in [*const.DASH, "to", "_"]:
                expected_len = 2

        factor = cls.factors_m[units_]

        elevation = round(values[0] * factor, 3)
        units_ = "m"

        # Handle an elevation range
        if expected_len > 1:
            hi = round(values[1] * factor, 3)

        return super().from_ent(
            ent,
            elevation=elevation,
            elevation_high=hi,
            units=units_,
            about=about,
        )


@registry.misc("elevation_match")
def elevation_match(ent):
    return Elevation.elevation_match(ent)
