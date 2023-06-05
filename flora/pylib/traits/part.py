import re
from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import ACCUMULATOR
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes.reject_match import REJECT_MATCH


PART_CSV = Path(__file__).parent / "terms" / "part_terms.csv"
MISSING_CSV = Path(__file__).parent / "terms" / "missing_terms.csv"
ALL_CSVS = [PART_CSV, MISSING_CSV]

REPLACE = term_util.term_data(ALL_CSVS, "replace")

NOT_PART = ["bad_part", "part_and", "part_leader", "part_missing", "subpart"]
PART_LABELS = [lb for lb in term_util.get_labels(PART_CSV) if lb not in NOT_PART]

OTHER_LABELS = "missing_part missing_subpart multiple_parts subpart".split()
ALL_LABELS = PART_LABELS + OTHER_LABELS


def build(nlp: Language):
    add.term_pipe(nlp, name="part_terms", path=ALL_CSVS)
    add.trait_pipe(nlp, name="part_patterns", compiler=part_patterns())
    overwrite = [*PART_LABELS, "subpart"]
    add.trait_pipe(
        nlp, name="subpart_patterns", compiler=subpart_patterns(), overwrite=overwrite
    )
    ACCUMULATOR.keep += ALL_LABELS
    add.cleanup_pipe(nlp, name="part_cleanup")


def part_patterns():
    decoder = {
        "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
        "and": {"ENT_TYPE": "part_and"},
        "bad_part": {"ENT_TYPE": "bad_part"},
        "leader": {"ENT_TYPE": "part_leader"},
        "missing": {"ENT_TYPE": "missing"},
        "part": {"ENT_TYPE": {"IN": PART_LABELS}},
    }

    return [
        Compiler(
            label="part",
            id="part",
            on_match="part_match",
            keep="part",
            decoder=decoder,
            patterns=[
                "leader? part+",
                "leader? part+ - part+",
            ],
        ),
        Compiler(
            label="missing_part",
            on_match="part_match",
            keep="missing_part",
            decoder=decoder,
            patterns=[
                "missing part+",
                "missing part+ and part+",
                "missing part+ -   part+",
            ],
        ),
        Compiler(
            label="multiple_parts",
            on_match="part_match",
            keep="multiple_parts",
            decoder=decoder,
            patterns=[
                "leader? part+ and part+",
                "missing part+ and part+",
            ],
        ),
        Compiler(
            label="not_a_part",
            on_match=REJECT_MATCH,
            decoder=decoder,
            patterns=[
                "- part+",
                "bad_part",
            ],
        ),
    ]


def subpart_patterns():
    decoder = {
        "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
        "leader": {"ENT_TYPE": "part_leader"},
        "missing": {"ENT_TYPE": "missing"},
        "part": {"ENT_TYPE": {"IN": PART_LABELS}},
        "subpart": {"ENT_TYPE": "subpart"},
    }

    return [
        Compiler(
            label="subpart",
            on_match="subpart_match",
            keep="subpart",
            decoder=decoder,
            patterns=[
                "leader? subpart+",
                "leader? subpart+ - subpart+",
                "leader? part+ -?   subpart+",
                "- subpart",
            ],
        ),
        Compiler(
            label="missing_subpart",
            on_match="subpart_match",
            keep="missing_subpart",
            decoder=decoder,
            patterns=[
                "missing part+ -?   subpart+",
                "missing part+      subpart+",
                "missing subpart+",
            ],
        ),
    ]


@registry.misc("part_match")
def part_match(ent):
    frags = [[]]
    label = ent.label_
    relabel = ent.label_

    for token in ent:
        token._.flag = "part"

        if relabel not in OTHER_LABELS and token._.term in PART_LABELS:
            relabel = token._.term

        if token._.term in ALL_LABELS:
            part = REPLACE.get(token.lower_, token.lower_)

            if part not in frags[-1]:
                frags[-1].append(part)

            if label not in ("missing_part", "multiple_parts", "subpart"):
                label = token._.term

        elif token._.term == "missing":
            frags[-1].append(REPLACE.get(token.lower_, token.lower_))

        elif token._.term == "part_and":
            frags.append([])

    all_parts = [" ".join(f) for f in frags]
    all_parts = [re.sub(r" - ", "-", p) for p in all_parts]
    all_parts = [REPLACE.get(p, p) for p in all_parts]

    ent._.relabel = relabel
    ent._.data = {
        "trait": relabel,
        relabel: all_parts[0] if len(all_parts) == 1 else all_parts,
    }

    ent[0]._.data = ent._.data  # Cache so we can use this later


@registry.misc("subpart_match")
def subpart_match(ent):
    frags = []

    for token in ent:
        token._.flag = "subpart"

        if token._.term in ALL_LABELS:
            part = REPLACE.get(token.lower_, token.lower_)

            if part not in frags:
                frags.append(part)

        elif token._.term == "missing":
            frags.append(REPLACE.get(token.lower_, token.lower_))

    subpart = " ".join(frags)
    subpart = re.sub(r" - ", "-", subpart)
    subpart = REPLACE.get(subpart, subpart)

    ent._.data = {
        "trait": "subpart",
        "subpart": subpart,
    }

    ent[0]._.data = ent._.data  # Cache so we can use this later
