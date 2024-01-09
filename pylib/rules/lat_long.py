import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const, term_util, util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

from .base import Base


@dataclass(eq=False)
class LatLong(Base):
    # Class vars ----------
    sym: ClassVar[str] = r"""°"”“'`‘´’"""
    punct: ClassVar[str] = f"""{sym},;._"""
    float_re: ClassVar[str] = r"\d+(\.\d+)?"
    float_ll: ClassVar[str] = r"\d{1,3}(\.\d+)?"
    plus: ClassVar[str] = r"^(±|\+|-|\+-|-\+)+\Z"
    minus: ClassVar[str] = r"^[-]\Z"
    datum_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "datum_terms.csv"
    lat_long_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "lat_long_terms.csv"
    )
    unit_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "unit_length_terms.csv"
    all_csvs: ClassVar[list[Path]] = [lat_long_csv, unit_csv, datum_csv]
    replace: ClassVar[dict[str, str]] = term_util.term_data(all_csvs, "replace")
    factors_cm: ClassVar[dict[str, float]] = term_util.term_data(
        unit_csv,
        "factor_cm",
        float,
    )
    factors_m: ClassVar[dict[str, float]] = {
        k: v / 100.0 for k, v in factors_cm.items()
    }
    dir_: ClassVar[str] = """((north|east|south|west)(ing)?|[nesw])"""
    # ---------------------

    lat_long: str = None
    datum: str = None
    units: str = None
    uncertainty: float = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(
            verbatimCoordinates=self._text,
            geodeticDatum=self.datum,
            coordinateUncertaintyInMeters=self.uncertainty,
        )

    @property
    def key(self):
        return DarwinCore.ns("verbatimCoordinates")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="lat_long_terms", path=cls.all_csvs)
        add.trait_pipe(nlp, name="lat_long_patterns", compiler=cls.lat_long_patterns())
        add.trait_pipe(
            nlp,
            name="lat_long_plus_patterns",
            overwrite=["lat_long"],
            compiler=cls.lat_long_plus_patterns(),
        )
        add.cleanup_pipe(nlp, name="lat_long_cleanup")

    @classmethod
    def lat_long_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": const.OPEN}},
            ")": {"TEXT": {"IN": const.CLOSE}},
            ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
            "/": {"TEXT": {"IN": const.SLASH}},
            "-": {"TEXT": {"IN": const.DASH}},
            "'s": {"LOWER": "'s"},
            "99": {"LOWER": {"REGEX": r"^\d{1,2}$"}},
            "9999": {"LOWER": {"REGEX": r"^\d+$"}},
            "99.0": {"TEXT": {"REGEX": rf"^{cls.float_ll}$"}},
            "99.99": {"TEXT": {"REGEX": r"^\d+\.\d{2,}$"}},
            "[+]": {"TEXT": {"REGEX": cls.plus}},
            "[-]": {"TEXT": {"REGEX": cls.plus}},
            "datum": {"ENT_TYPE": "datum"},
            "datum_label": {"ENT_TYPE": "datum_label"},
            "deg": {"LOWER": {"REGEX": rf"""^([{cls.sym}]|degrees?|deg\.?|d)\Z"""}},
            "dir": {"LOWER": {"REGEX": r"""^'?[nesw]\.?\Z"""}},
            "dir99.0": {"LOWER": {"REGEX": rf"""^[nesw]{cls.float_ll}\Z"""}},
            "key": {"ENT_TYPE": "lat_long_key"},
            "label": {"ENT_TYPE": "lat_long_label"},
            "m": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
            "min": {"LOWER": {"REGEX": rf"""^([{cls.sym}]|minutes?|min\.?|m)\Z"""}},
            "sec": {"LOWER": {"REGEX": rf"""^([{cls.sym}]|seconds?|sec\.?|s)\Z"""}},
            "sect": {"LOWER": {"REGEX": r"""^(section|sec\.?|s)$"""}},
            "sp": {"IS_SPACE": True},
            "uncert": {"ENT_TYPE": "uncertain_label"},
        }

        return [
            Compiler(
                label="lat_long",
                on_match="lat_long_match",
                keep="lat_long",
                decoder=decoder,
                patterns=[
                    (
                        "label* sp? [-]? 99.0 deg 99.0? min* 99.0? sec* ,* sp? "
                        "           [-]? 99.0 deg 99.0? min* 99.0? sec* (? datum* )?"
                    ),
                    (
                        "label* sp? [-]? 99.0 deg* 99.0? min* 99.0? sec* dir  ,* sp? "
                        "           [-]? 99.0 deg* 99.0? min* 99.0? sec* dir  "
                        "(? datum* )?"
                    ),
                    (
                        "label* sp? dir [-]? 99.0 deg* 99.0? min* 99.0? sec* ,* sp? "
                        "           dir [-]? 99.0 deg* 99.0? min* 99.0? sec* "
                        "(? datum* )?"
                    ),
                    (
                        "key ,* [-]? 99.0 deg* 99.0? min* 99.0? sec* dir? ,* sp? "
                        "key ,* [-]? 99.0 deg* 99.0? min* 99.0? sec* dir? (? datum* )?"
                    ),
                    (
                        "[-]? 99.0 deg* 99.0? min* 99.0? sec* dir? key ,* sp? "
                        "[-]? 99.0 deg* 99.0? min* 99.0? sec* dir? key ,* (? datum* )?"
                    ),
                    (
                        "key ,* [-]? 99.0 deg* 99.0? min* 99.0? sec* dir? [-] sp? "
                        "99.0 deg* 99.0? min* 99.0? sec* dir? ,*  sp? "
                        "key ,* [-]? 99.0 deg* 99.0? min* 99.0? sec* dir? [-] sp? "
                        "99.0 deg* 99.0? min* 99.0? sec* dir? (? datum* )?"
                    ),
                    (
                        "label* sp? dir99.0 deg* 99.0? min* 99.0? sec* ,* sp? "
                        "           dir99.0 deg* 99.0? min* 99.0? sec* (? datum* )?"
                    ),
                    (
                        "label* sp? [-]? 99.0 deg 99.0? min* -? 99.0? sec* dir? ,* sp? "
                        "          [-]? 99.0 deg 99.0? min* -? 99.0? sec* dir? "
                        "(? datum* )?"
                    ),
                    (
                        "label* sp? [-]? 99.0 deg 99.0? min* -? 99.0? 's ,* sp? "
                        "          [-]? 99.0 deg 99.0? min* -? 99.0? sec* dir? "
                        "(? datum* )?"
                    ),
                    "label* sp? [-]? 99.99 dir? ,* sp? [-]? 99.99 dir? (? datum* )?",
                ],
            ),
        ]

    @classmethod
    def lat_long_plus_patterns(cls):
        decoder = {
            "-": {"TEXT": {"IN": const.DASH}},
            ",": {"TEXT": {"REGEX": r"^[,;._:]\Z"}},
            "(": {"TEXT": {"IN": const.OPEN}},
            ")": {"TEXT": {"IN": const.CLOSE}},
            "datum": {"ENT_TYPE": "datum"},
            "datum_label": {"ENT_TYPE": "datum_label"},
            "m": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
            "99.0": {"TEXT": {"REGEX": rf"^{cls.float_re}$"}},
            "+99.0": {"TEXT": {"REGEX": r"^(±|\+|-)?\d+(\.\d+)?\Z"}},
            "uncert": {"ENT_TYPE": "uncertain_label"},
            "lat_long": {"ENT_TYPE": "lat_long"},
            "[+]": {"TEXT": {"REGEX": cls.plus}},
            "99": {"IS_DIGIT": True},
        }
        return [
            Compiler(
                label="lat_long_uncertain",
                id="lat_long",
                on_match="lat_long_uncertain",
                keep=["lat_long"],
                decoder=decoder,
                patterns=[
                    "lat_long+                            datum_label+ ,* (? datum+ )?",
                    "lat_long+ ,? uncert? ,?   +99.0 m ,* datum_label* ,* (? datum* )?",
                    (
                        "lat_long+ ,? uncert? ,? [+]* 99.0 m ,* "
                        "datum_label* ,* (? datum* )?"
                    ),
                    (
                        "lat_long+ ,? uncert? ,? [+]* 99.0 - 99.0 m ,* "
                        "datum_label* ,* (? datum* )?"
                    ),
                ],
            ),
        ]

    @classmethod
    def format_coords(cls, frags):
        coords = " ".join(frags)
        coords = re.sub(rf"\s([{cls.punct}])", r"\1", coords)
        coords = re.sub(r"\s(:)", r"\1", coords)
        coords = re.sub(r"(?<=\d)([NESWnesw])", r" \1", coords)
        coords = re.sub(r"-\s(?=\d)", r"-", coords)
        return " ".join(coords.split())

    @classmethod
    def lat_long_match(cls, ent):
        frags = []
        datum = []
        for token in ent:
            token._.flag = "lat_long"

            if token._.term == "lat_long_label":
                continue

            if token.text in const.OPEN + const.CLOSE:
                continue

            if token._.term == "datum":
                datum.append(token.lower_)

            else:
                text = token.text.upper() if len(token.text) == 1 else token.text
                frags.append(text)

        lat_long = cls.format_coords(frags)

        if datum:
            datum = "".join(datum)
            datum = cls.replace.get(datum, datum)
        else:
            datum = None

        ent[0]._.flag = "lat_long_data"

        trait = super().from_ent(ent, lat_long=lat_long, datum=datum)
        ent[0]._.trait = trait  # Save for uncertainty in the lat/long
        return trait

    @classmethod
    def lat_long_uncertain(cls, ent):
        value = 0.0
        unit = []
        datum = []
        kwargs = {}

        for token in ent:
            # Get the data from the original parse
            if token._.flag == "lat_long_data":
                kwargs = asdict(token._.trait)

            # Get the uncertainty units
            elif token._.term in ("metric_length", "imperial_length"):
                unit.append(token.lower_)

            # Already parsed
            elif token._.flag:
                continue

            # Pick up a trailing datum
            elif token._.term == "datum":
                datum.append(token.lower_)

            # Get the uncertainty value
            elif re.match(const.FLOAT_RE, token.text):
                value = util.to_positive_float(token.text)

        if value and not unit:
            raise reject_match.RejectMatch

        # Convert the values to meters
        if value:
            unit = "".join(unit)
            unit = cls.replace.get(unit, unit)
            kwargs["units"] = "m"
            factor = cls.factors_m[unit]
            kwargs["uncertainty"] = round(value * factor, 3)
        else:
            kwargs["units"] = None
            kwargs["uncertainty"] = None

        datum = "".join(datum)
        kwargs["datum"] = cls.replace.get(datum, datum) if datum else None

        trait = super().from_ent(ent, **kwargs)
        trait.trait = "lat_long"
        return trait


@registry.misc("lat_long_match")
def lat_long_match(ent):
    return LatLong.lat_long_match(ent)


@registry.misc("lat_long_uncertain")
def lat_long_uncertain(ent):
    return LatLong.lat_long_uncertain(ent)
