from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits.linker import Linker


@dataclass(eq=False)
class PartLocationLinker(Linker):
    # Class vars ----------
    link_location_parents: ClassVar[list[str]] = ["part_location"]
    link_location_children: ClassVar[
        list[str]
    ] = """
        color count joined margin multiple_parts part shape size
        subpart surface venation woodiness
        """.split()
    # ---------------------

    @classmethod
    def pipe(cls, nlp: Language):
        add.link_pipe(
            nlp,
            name="link_location",
            compiler=cls.link_location_patterns(),
            parents=cls.link_location_parents,
            children=cls.link_location_children,
            weights=t_const.TOKEN_WEIGHTS,
        )

    @classmethod
    def link_location_patterns(cls):
        return Compiler(
            label="link_location",
            decoder={
                "part_location": {"ENT_TYPE": {"IN": cls.link_location_parents}},
                "trait": {"ENT_TYPE": {"IN": cls.link_location_children}},
                "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
            },
            patterns=[
                "trait    clause* part_location",
                "part_location clause* trait",
            ],
        )
