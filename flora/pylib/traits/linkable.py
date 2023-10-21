from dataclasses import dataclass

from spacy.language import Language
from traiter.pylib.traits import base as t_base


@dataclass
class Linkable(t_base.Base):
    part: str | list[str] = None
    subpart: str = None
    sex: str = None
    location: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError
