"""Link traits to plant subparts."""
from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.linker import Linker


@dataclass(eq=False)
class SubpartLinker(Linker):
    # Class vars ----------
    parents: ClassVar[list[str]] = ["subpart"]
    children: ClassVar[list[str]] = """
        color duration duration margin shape surface venation woodiness
        """.split()
    child_once: ClassVar[list[str]] = ["size", "count"]

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
            parents=cls.parents,
            children=cls.children,
            weights=t_const.TOKEN_WEIGHTS,
        )

        add.link_pipe(
            nlp,
            name="link_subpart_once",
            compiler=cls.link_subpart_once_patterns(),
            parents=cls.parents,
            children=cls.child_once,
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
                "subpart": {"ENT_TYPE": {"IN": cls.parents}},
                "trait": {"ENT_TYPE": {"IN": cls.children}},
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
                "subpart": {"ENT_TYPE": {"IN": cls.parents}},
                "trait": {"ENT_TYPE": {"IN": cls.child_once}},
            },
            patterns=[
                "trait+    any* subpart+",
                "subpart+  any* trait+",
            ],
        )
