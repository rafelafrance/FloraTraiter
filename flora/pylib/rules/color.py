from dataclasses import dataclass

from spacy import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.rules import color as t_color

from .linkable import Linkable


# Do what the traiter.Color does but add fields (via Linkable),
# so we can link parts etc. to it.
@dataclass(eq=False)
class Color(t_color.Color, Linkable):
    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.color})

    @property
    def key(self) -> str:
        prepend = "missing" if self.missing else None
        return self.key_builder("color", prepend=prepend)

    @classmethod
    def color_match(cls, ent):
        return super().color_match(ent)


@registry.misc("color_match")
def color_match(ent):
    return Color.color_match(ent)
