"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from . import part

CHILDREN = """
    color duration duration margin shape surface venation woodiness
    """.split()

LINK_PART_PARENTS = part.PART_LABELS + ["multiple_parts"]
LINK_PART_CHILDREN = CHILDREN + ["subpart"]
LINK_PART_ONCE_CHILDREN = ["size", "count"]

LINK_SUBPART_PARENTS = ["subpart"]
LINK_SUBPART_CHILDREN = CHILDREN


DECODER = {
    "any": {},
    "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
}


def build(nlp: Language):
    add.link_pipe(
        nlp,
        name="link_part",
        compiler=link_part_patterns(),
        parents=LINK_PART_PARENTS,
        children=LINK_PART_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        reverse_weights=t_const.REVERSE_WEIGHTS,
    )

    add.link_pipe(
        nlp,
        name="link_part_once",
        compiler=link_part_once_patterns(),
        parents=LINK_PART_PARENTS,
        children=LINK_PART_ONCE_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        max_links=1,
        differ=["sex", "dimensions"],
    )

    add.link_pipe(
        nlp,
        name="link_subpart",
        compiler=link_subpart_patterns(),
        parents=LINK_SUBPART_PARENTS,
        children=LINK_SUBPART_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
    )

    add.link_pipe(
        nlp,
        name="link_subpart_once",
        compiler=link_subpart_once_patterns(),
        parents=LINK_SUBPART_PARENTS,
        children=LINK_PART_ONCE_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
        max_links=1,
        differ=["sex", "dimensions"],
    )


def link_part_patterns():
    return Compiler(
        label="link_part",
        decoder=DECODER
        | {
            "part": {"ENT_TYPE": {"IN": LINK_PART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_PART_CHILDREN}},
        },
        patterns=[
            "trait+ any* part+",
            "part+  any* trait+",
        ],
    )


def link_part_once_patterns():
    return Compiler(
        label="link_part_once",
        decoder=DECODER
        | {
            "part": {"ENT_TYPE": {"IN": LINK_PART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_PART_ONCE_CHILDREN}},
        },
        patterns=[
            "trait+ any* part+",
            "part+  any* trait+",
        ],
    )


def link_subpart_patterns():
    return Compiler(
        label="link_subpart",
        decoder=DECODER
        | {
            "subpart": {"ENT_TYPE": {"IN": LINK_SUBPART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_SUBPART_CHILDREN}},
        },
        patterns=[
            "trait+   clause* subpart+",
            "subpart+ clause* trait+",
        ],
    )


def link_subpart_once_patterns():
    return Compiler(
        label="link_subpart_once",
        decoder=DECODER
        | {
            "part": {"ENT_TYPE": {"IN": LINK_SUBPART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_PART_ONCE_CHILDREN}},
        },
        patterns=[
            "trait+ any* part+",
            "part+  any* trait+",
        ],
    )
