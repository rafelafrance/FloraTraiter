from dataclasses import dataclass
from typing import ClassVar

from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits.linker import Linker


@dataclass
class TaxonLikeLinker(Linker):
    # Class vars ----------
    taxon_like_parents: ClassVar[list[str]] = ["taxon_like"]
    taxon_like_children: ClassVar[list[str]] = ["taxon"]
    # ---------------------

    @classmethod
    def pipe(cls, nlp: Language):
        add.link_pipe(
            nlp,
            name="link_taxon_like_patterns",
            compiler=cls.link_taxon_like_patterns(),
            parents=cls.taxon_like_parents,
            children=cls.taxon_like_children,
            weights=t_const.TOKEN_WEIGHTS,
        )

    @classmethod
    def link_taxon_like_patterns(cls):
        return Compiler(
            label="link_taxon_like",
            decoder={
                "any": {},
                "taxon_like": {"ENT_TYPE": {"IN": cls.taxon_like_parents}},
                "taxon": {"ENT_TYPE": {"IN": cls.taxon_like_children}},
            },
            patterns=[
                "taxon      any* taxon_like",
                "taxon_like any* taxon",
            ],
        )
