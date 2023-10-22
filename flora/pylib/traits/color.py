from dataclasses import dataclass

from traiter.pylib.traits import color as t_color

from .linkable import Linkable


# Do what the traiter.Color does but add fields, so we can link parts etc. to it.
@dataclass
class Color(t_color.Color, Linkable):
    ...
