from dataclasses import dataclass
from pathlib import Path

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from .linkable import Linkable


@dataclass(eq=False)
class Surface(Linkable):
    # Class vars ----------
    surface_csv = Path(__file__).parent / "terms" / "surface_terms.csv"
    replace = term_util.term_data(surface_csv, "replace")
    # ---------------------

    surface: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.surface})

    @property
    def key(self) -> str:
        return self.key_builder("surface")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="surface_terms", path=cls.surface_csv)
        add.trait_pipe(nlp, name="surface_patterns", compiler=cls.surface_patterns())
        add.cleanup_pipe(nlp, name="surface_cleanup")

    @classmethod
    def surface_patterns(cls):
        return [
            Compiler(
                label="surface",
                on_match="surface_match",
                keep="surface",
                decoder={
                    "-": {"TEXT": {"IN": t_const.DASH}},
                    "surface": {"ENT_TYPE": "surface_term"},
                    "surface_leader": {"ENT_TYPE": "surface_leader"},
                },
                patterns=[
                    "                  surface",
                    "surface_leader -? surface",
                ],
            ),
        ]

    @classmethod
    def surface_match(cls, ent):
        surface = {}  # Dicts preserve order sets do not
        for token in ent:
            if token._.term == "surface_term" and token.text != "-":
                word = cls.replace.get(token.lower_, token.lower_)
                surface[word] = 1
        surface = " ".join(surface)
        surface = cls.replace.get(surface, surface)
        return cls.from_ent(ent, surface=surface)


@registry.misc("surface_match")
def surface_match(ent):
    return Surface.surface_match(ent)
