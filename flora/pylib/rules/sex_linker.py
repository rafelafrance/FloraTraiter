"""
Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.linker import Linker


@dataclass(eq=False)
class SexLinker(Linker):
    # Class vars ----------
    parents: ClassVar[list[str]] = ["sex"]
    children: ClassVar[list[str]] = """
        color count duration duration flower_location habit
        joined leaf_duration leaf_folding part_location flower_morphology
        margin multiple_parts part_location part plant_morphology shape
        size subpart surface venation woodiness
        """.split()
    # ---------------------

    @classmethod
    def pipe(cls, nlp: Language):
        add.link_pipe(
            nlp,
            name="link_sex",
            compiler=cls.link_sex_patterns(),
            parents=cls.parents,
            children=cls.children,
            weights=t_const.TOKEN_WEIGHTS,
        )

    @classmethod
    def link_sex_patterns(cls):
        return Compiler(
            label="link_sex",
            decoder={
                "sex": {"ENT_TYPE": {"IN": cls.parents}},
                "trait": {"ENT_TYPE": {"IN": cls.children}},
                "phrase": {"TEXT": {"NOT_IN": list(".;:")}},
            },
            patterns=[
                "trait phrase* sex",
                "sex   phrase* trait",
            ],
        )
