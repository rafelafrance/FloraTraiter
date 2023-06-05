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

LINK_SEX_PARENTS = ["sex"]
LINK_SEX_CHILDREN = """
    color count duration duration flower_location flower_part fruit_part habit habitat
    inflorescence joined leaf_duration leaf_folding leaf_part location flower_morphology
    male_flower_part margin multiple_parts part_as_loc
    plant_morphology plant_part shape size subpart subpart_as_loc subpart_suffix
    surface venation woodiness
    """.split()


def build(nlp: Language):
    add.link_pipe(
        nlp,
        name="link_sex",
        compiler=link_sex_patterns(),
        parents=LINK_SEX_PARENTS,
        children=LINK_SEX_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
    )


def link_sex_patterns():
    return Compiler(
        label="link_sex",
        decoder={
            "sex": {"ENT_TYPE": {"IN": LINK_SEX_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_SEX_CHILDREN}},
            "phrase": {"TEXT": {"NOT_IN": list(".;:")}},
        },
        patterns=[
            "trait phrase* sex",
            "sex   phrase* trait",
        ],
    )
