from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util as tu
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules import terms as t_terms

from .linkable import Linkable


@dataclass(eq=False)
class PartLocation(Linkable):
    # Class vars ----------
    location_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "part_location_terms.csv"
    )
    units_csv: ClassVar[Path] = Path(t_terms.__file__).parent / "unit_length_terms.csv"
    all_csvs: ClassVar[list[Path]] = [location_csv, units_csv]

    replace: ClassVar[dict[str, str]] = tu.term_data(location_csv, "replace")
    overwrite: ClassVar[list[str]] = [
        "part",
        "subpart",
        *tu.get_labels(location_csv),
        *tu.get_labels(units_csv),
    ]
    # ---------------------

    part_location: str = None
    type: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.part_location})

    @property
    def key(self) -> str:
        return self.key_builder(*self.type.split("_"))

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="location_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="location_patterns",
            compiler=cls.location_patterns(),
            overwrite=cls.overwrite,
        )
        add.cleanup_pipe(nlp, name="part_location_cleanup")

    @classmethod
    def location_patterns(cls):
        decoder = {
            "9.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
            "-/to": {"LOWER": {"IN": [*t_const.DASH, "to", "_"]}},
            "adj": {"POS": "ADJ"},
            "cm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
            "joined": {"ENT_TYPE": "joined"},
            "leader": {"ENT_TYPE": "location_leader"},
            "location": {"ENT_TYPE": "location"},
            "missing": {"ENT_TYPE": "missing"},
            "of": {"LOWER": "of"},
            "part": {"ENT_TYPE": "part"},
            "prep": {"POS": {"IN": ["ADP", "CCONJ"]}},
            "sp": {"IS_SPACE": True},
            "subpart": {"ENT_TYPE": "subpart"},
        }
        return [
            Compiler(
                label="part_as_location",
                id="part_location",
                on_match="part_as_location_match",
                decoder=decoder,
                keep="part_location",
                patterns=[
                    "missing? joined?  leader prep? part",
                    "missing? location leader       part",
                    "                  leader       part prep? missing? joined",
                ],
            ),
            Compiler(
                label="subpart_as_location",
                id="part_location",
                on_match="subpart_as_location_match",
                decoder=decoder,
                keep="part_location",
                patterns=[
                    "missing? joined?  leader subpart",
                    "missing? joined?  leader subpart sp? of adj? sp? subpart",
                    "missing? location leader subpart",
                    "missing? location leader subpart sp? of adj? sp? subpart",
                ],
            ),
            Compiler(
                label="part_as_distance",
                id="part_location",
                on_match="part_as_distance_match",
                keep="part_location",
                decoder=decoder,
                patterns=[
                    "missing? joined?  leader prep? part prep? 9.9 -/to* 9.9? cm",
                    "missing? location leader prep? part prep? 9.9 -/to* 9.9? cm",
                ],
            ),
            Compiler(
                label="part_location",
                id="part_location",
                on_match="part_location_match",
                keep="part_location",
                decoder=decoder,
                patterns=[
                    "location+",
                ],
            ),
        ]

    @classmethod
    def loc(cls, ent):
        location = " ".join([cls.replace.get(t.lower_, t.lower_) for t in ent])
        return " ".join(location.split())

    @classmethod
    def part_as_distance_match(cls, ent):
        return cls.from_ent(ent, type="part_as_distance", part_location=cls.loc(ent))

    @classmethod
    def part_as_location_match(cls, ent):
        return cls.from_ent(ent, type="part_as_location", part_location=cls.loc(ent))

    @classmethod
    def subpart_as_location_match(cls, ent):
        return cls.from_ent(ent, type="subpart_as_location", part_location=cls.loc(ent))

    @classmethod
    def part_location_match(cls, ent):
        return cls.from_ent(ent, type="part_location", part_location=cls.loc(ent))


@registry.misc("part_as_distance_match")
def part_as_distance_match(ent):
    return PartLocation.part_as_distance_match(ent)


@registry.misc("part_as_location_match")
def part_as_location_match(ent):
    return PartLocation.part_as_location_match(ent)


@registry.misc("subpart_as_location_match")
def subpart_as_location_match(ent):
    return PartLocation.subpart_as_location_match(ent)


@registry.misc("part_location_match")
def part_location_match(ent):
    return PartLocation.part_location_match(ent)
