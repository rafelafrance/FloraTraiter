from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.linker import Linker


@dataclass(eq=False)
class TaxonLikeLinker(Linker):
    # Class vars ----------
    parents: ClassVar[list[str]] = ["taxon_like"]
    children: ClassVar[list[str]] = ["taxon"]
    # ---------------------

    @classmethod
    def pipe(cls, nlp: Language):
        add.link_pipe(
            nlp,
            name="link_taxon_like_patterns",
            compiler=cls.link_taxon_like_patterns(),
            parents=cls.parents,
            children=cls.children,
            weights=t_const.TOKEN_WEIGHTS,
        )

    @classmethod
    def link_taxon_like_patterns(cls):
        return Compiler(
            label="link_taxon_like",
            decoder={
                "any": {},
                "taxon_like": {"ENT_TYPE": {"IN": cls.parents}},
                "taxon": {"ENT_TYPE": {"IN": cls.children}},
            },
            patterns=[
                "taxon      any* taxon_like",
                "taxon_like any* taxon",
            ],
        )
