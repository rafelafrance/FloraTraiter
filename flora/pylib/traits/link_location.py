from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

LINK_LOCATION_PARENTS = ["location"]

LINK_LOCATION_CHILDREN = """
    color count joined leaf_folding
    flower_morphology margin multiple_parts part plant_morphology
    shape size subpart subpart_suffix surface venation woodiness
    """.split()


def build(nlp: Language):
    add.link_pipe(
        nlp,
        name="link_location",
        compiler=link_location_patterns(),
        parents=LINK_LOCATION_PARENTS,
        children=LINK_LOCATION_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
    )


def link_location_patterns():
    return Compiler(
        label="link_location",
        decoder={
            "location": {"ENT_TYPE": {"IN": LINK_LOCATION_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_LOCATION_CHILDREN}},
            "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
        },
        patterns=[
            "trait    clause* location",
            "location clause* trait",
        ],
    )
