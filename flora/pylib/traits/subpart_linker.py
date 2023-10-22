"""Link traits to plant subparts."""
from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits.linker import Linker


@dataclass
class SubpartLinker(Linker):
    # Class vars ----------
    link_subpart_parents: ClassVar[list[str]] = ["subpart"]
    link_subpart_children: ClassVar[
        list[str]
    ] = """
        color duration duration margin shape surface venation woodiness
        """.split()
    link_subpart_once_children: ClassVar[list[str]] = ["size", "count"]

    decoder: ClassVar[dict[str, dict]] = {
        "any": {},
        "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
    }
    # ---------------------

    @classmethod
    def pipe(cls, nlp: Language):
        add.link_pipe(
            nlp,
            name="link_subpart",
            compiler=cls.link_subpart_patterns(),
            parents=cls.link_subpart_parents,
            children=cls.link_subpart_children,
            weights=t_const.TOKEN_WEIGHTS,
        )

        add.link_pipe(
            nlp,
            name="link_subpart_once",
            compiler=cls.link_subpart_once_patterns(),
            parents=cls.link_subpart_parents,
            children=cls.link_subpart_once_children,
            weights=t_const.TOKEN_WEIGHTS,
            max_links=1,
            differ=["sex", "dimensions"],
        )

    @classmethod
    def link_subpart_patterns(cls):
        return Compiler(
            label="link_subpart",
            decoder=cls.decoder
            | {
                "subpart": {"ENT_TYPE": {"IN": cls.link_subpart_parents}},
                "trait": {"ENT_TYPE": {"IN": cls.link_subpart_children}},
            },
            patterns=[
                "trait+   clause* subpart+",
                "subpart+ clause* trait+",
            ],
        )

    @classmethod
    def link_subpart_once_patterns(cls):
        return Compiler(
            label="link_subpart_once",
            decoder=cls.decoder
            | {
                "subpart": {"ENT_TYPE": {"IN": cls.link_subpart_parents}},
                "trait": {"ENT_TYPE": {"IN": cls.link_subpart_once_children}},
            },
            patterns=[
                "trait+    any* subpart+",
                "subpart+  any* trait+",
            ],
        )
