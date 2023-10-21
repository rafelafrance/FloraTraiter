from dataclasses import dataclass

from traiter.pylib.traits import color as t_color

from .linkable import Linkable


@dataclass
class Color(t_color.Color, Linkable):
    ...
