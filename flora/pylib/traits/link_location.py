"""Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add


LINK_LOCATION_PART_PARENTS = (
    """ location flower_location part_as_loc part_as_distance """.split()
)
LINK_LOCATION_PART_CHILDREN = """
    color count duration duration flower_part fruit_part habit habitat
    inflorescence joined leaf_duration leaf_folding leaf_part flower_morphology
    margin multiple_parts plant_part plant_duration plant_morphology reproduction
    shape size subpart subpart_suffix surface venation woodiness
    """.split()

LINK_LOCATION_SUBPART_PARENTS = """ subpart_as_loc part_as_distance """.split()
LINK_LOCATION_SUBPART_CHILDREN = """
    color count duration duration flower_part fruit_part habit habitat
    inflorescence joined leaf_duration leaf_folding leaf_part flower_morphology
    margin multiple_parts plant_part plant_duration plant_morphology reproduction
    shape size subpart_suffix surface venation woodiness
    """.split()


def build(nlp: Language):
    add.link_pipe(
        nlp,
        name="link_location_part",
        compiler=link_location_patterns(),
        parents=LINK_LOCATION_PART_PARENTS,
        children=LINK_LOCATION_PART_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
    )

    add.link_pipe(
        nlp,
        name="link_location_subpart",
        compiler=link_location_subpart_patterns(),
        parents=LINK_LOCATION_SUBPART_PARENTS,
        children=LINK_LOCATION_SUBPART_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
    )


def link_location_patterns():
    return Compiler(
        label="link_location_part",
        decoder={
            "location": {"ENT_TYPE": {"IN": LINK_LOCATION_PART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_LOCATION_PART_CHILDREN}},
            "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
        },
        patterns=[
            "trait    clause* location",
            "location clause* trait",
        ],
    )


def link_location_subpart_patterns():
    return Compiler(
        label="link_location_subpart",
        id="link_location",
        decoder={
            "location": {"ENT_TYPE": {"IN": LINK_LOCATION_SUBPART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_LOCATION_SUBPART_CHILDREN}},
            "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
        },
        patterns=[
            "trait    clause* location",
            "location clause* trait",
        ],
    )
