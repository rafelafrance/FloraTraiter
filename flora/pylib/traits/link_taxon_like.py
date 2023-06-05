from spacy.language import Language
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

TAXON_LIKE_PARENTS = ["taxon_like"]
TAXON_LIKE_CHILDREN = ["taxon"]


def build(nlp: Language):
    add.link_pipe(
        nlp,
        name="link_taxon_like_patterns",
        compiler=link_taxon_like_patterns(),
        parents=TAXON_LIKE_PARENTS,
        children=TAXON_LIKE_CHILDREN,
        weights=t_const.TOKEN_WEIGHTS,
    )


def link_taxon_like_patterns():
    return Compiler(
        label="link_taxon_like",
        decoder={
            "any": {},
            "taxon_like": {"ENT_TYPE": {"IN": TAXON_LIKE_PARENTS}},
            "taxon": {"ENT_TYPE": {"IN": TAXON_LIKE_CHILDREN}},
        },
        patterns=[
            "taxon      any* taxon_like",
            "taxon_like any* taxon",
        ],
    )
