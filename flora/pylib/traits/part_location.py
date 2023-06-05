from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits import terms as t_terms

from .part import PART_LABELS


LOCATION_ENTS = """
    location flower_location part_as_loc subpart_as_loc part_as_distance
    """.split()

TO = ["to"]

PART_LOCATION_CSV = Path(__file__).parent / "terms" / "part_location_terms.csv"
UNITS_CSV = Path(t_terms.__file__).parent / "unit_length_terms.csv"
ALL_CSVS = [PART_LOCATION_CSV, UNITS_CSV]

REPLACE = term_util.term_data(PART_LOCATION_CSV, "replace")


def build(nlp: Language):
    add.term_pipe(nlp, name="part_location_terms", path=ALL_CSVS)
    add.trait_pipe(
        nlp,
        name="part_location_patterns",
        compiler=part_location_patterns(),
        overwrite=[*PART_LABELS, "subpart"],
    )
    add.cleanup_pipe(nlp, name="part_location_cleanup")


def part_location_patterns():
    decoder = {
        "9.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
        "-/to": {"LOWER": {"IN": t_const.DASH + TO + ["_"]}},
        "adj": {"POS": "ADJ"},
        "cm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
        "joined": {"ENT_TYPE": "joined"},
        "leader": {"ENT_TYPE": "location_leader"},
        "location": {"ENT_TYPE": {"IN": LOCATION_ENTS}},
        "missing": {"ENT_TYPE": "missing"},
        "of": {"LOWER": "of"},
        "part": {"ENT_TYPE": {"IN": PART_LABELS}},
        "prep": {"POS": {"IN": ["ADP", "CCONJ"]}},
        "subpart": {"ENT_TYPE": "subpart"},
    }

    return [
        Compiler(
            label="part_as_loc",
            on_match="part_location_match",
            decoder=decoder,
            keep=LOCATION_ENTS,
            patterns=[
                "missing? joined?  leader prep? part",
                "missing? location leader       part",
                "                  leader       part prep? missing? joined",
            ],
        ),
        Compiler(
            label="subpart_as_loc",
            on_match="part_location_match",
            keep=LOCATION_ENTS,
            decoder=decoder,
            patterns=[
                "missing? joined?  leader subpart",
                "missing? joined?  leader subpart of adj? subpart",
                "missing? location leader subpart",
                "missing? location leader subpart of adj? subpart",
            ],
        ),
        Compiler(
            label="part_as_distance",
            on_match="part_location_match",
            keep=LOCATION_ENTS,
            decoder=decoder,
            patterns=[
                "missing? joined?  leader prep? part prep? 9.9 -/to* 9.9? cm",
                "missing? location leader prep? part prep? 9.9 -/to* 9.9? cm",
            ],
        ),
    ]


@registry.misc("part_location_match")
def part_location_match(ent):
    frags = []
    for token in ent:
        frag = REPLACE.get(token.lower_, token.lower_)
        frags.append(frag)
    ent._.data = {ent.label_: " ".join(frags)}
