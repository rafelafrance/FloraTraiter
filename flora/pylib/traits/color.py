from dataclasses import dataclass

from spacy import registry
from traiter.pylib.traits import color as t_color

from .linkable import Linkable


# Do what the traiter.Color does but add fields, so we can link parts etc. to it.
@dataclass
class Color(t_color.Color, Linkable):
    @classmethod
    def color_trait(cls, ent):
        return super().color_trait(ent)


@registry.misc("color_trait")
def color_trait(ent):
    return Color.color_trait(ent)
