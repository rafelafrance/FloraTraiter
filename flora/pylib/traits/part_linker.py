"""Link traits to plant subparts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits.linker import Linker


@dataclass(eq=False)
class PartLinker(Linker):
    # Class vars ----------
    children_part_subpart: ClassVar[
        list[str]
    ] = """
        color duration duration margin shape surface venation woodiness
        """.split()

    link_part_parents: ClassVar[list[str]] = ["part", "multiple_parts"]
    link_part_children: ClassVar[list[str]] = [*children_part_subpart, "subpart"]
    link_part_once_children: ClassVar[list[str]] = ["size", "count"]

    decoder: ClassVar[dict[str, dict]] = {
        "any": {},
        "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
    }
    # ---------------------

    @classmethod
    def pipe(cls, nlp: Language):
        add.link_pipe(
            nlp,
            name="link_part",
            compiler=cls.link_part_patterns(),
            parents=cls.link_part_parents,
            children=cls.link_part_children,
            weights=t_const.TOKEN_WEIGHTS,
            reverse_weights=t_const.REVERSE_WEIGHTS,
        )

        add.link_pipe(
            nlp,
            name="link_part_once",
            compiler=cls.link_part_once_patterns(),
            parents=cls.link_part_parents,
            children=cls.link_part_once_children,
            weights=t_const.TOKEN_WEIGHTS,
            max_links=1,
            differ=["sex", "dimensions"],
        )

    @classmethod
    def link_part_patterns(cls):
        return Compiler(
            label="link_part",
            decoder=cls.decoder
            | {
                "part": {"ENT_TYPE": {"IN": cls.link_part_parents}},
                "trait": {"ENT_TYPE": {"IN": cls.link_part_children}},
            },
            patterns=[
                "trait+ any* part+",
                "part+  any* trait+",
            ],
        )

    @classmethod
    def link_part_once_patterns(cls):
        return Compiler(
            label="link_part_once",
            decoder=cls.decoder
            | {
                "part": {"ENT_TYPE": {"IN": cls.link_part_parents}},
                "trait": {"ENT_TYPE": {"IN": cls.link_part_once_children}},
            },
            patterns=[
                "trait+ any* part+",
                "part+  any* trait+",
            ],
        )
