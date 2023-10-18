from dataclasses import dataclass

from traiter.pylib.traits import base as t_base


@dataclass
class Base(t_base.Base):
    part: str | list[str] = None
    subpart: str = None
    sex: str = None
    location: str = None
    dimensions: str | list[str] = None
