from dataclasses import dataclass

from spacy import registry
from traiter.pylib.traits import color as t_color

from .linkable import Linkable


# Do what the traiter.Color does but add fields (via Linkable),
# so we can link parts etc. to it.
@dataclass(eq=False)
class Color(t_color.Color, Linkable):
    def to_dwc(self, dwc) -> None:
        dwc.add_dyn(**{self.key: self.color})

    @property
    def key(self):
        prepend = "missing" if self.missing else None
        return self.key_builder("color", prepend=prepend)

    @classmethod
    def color_trait(cls, ent):
        return super().color_trait(ent)


@registry.misc("color_trait")
def color_trait(ent):
    return Color.color_trait(ent)
