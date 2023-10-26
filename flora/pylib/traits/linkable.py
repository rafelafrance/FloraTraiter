from dataclasses import dataclass

from spacy.language import Language
from traiter.pylib.traits import base as t_base


@dataclass
class Linkable(t_base.Base):
    part: str | list[str] = None
    subpart: str = None
    sex: str = None
    part_location: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError

    # Examples: femaleFlowerPistolShape or stemSizeInCentimeters
    def dwc_key(self, *args, prepend: str = None) -> str:
        key = [prepend] if prepend else []
        for field in (self.sex, self.part, self.subpart):
            if field is not None:
                key += field.split()
        key += list(args)
        dupe = {k: 1 for k in key}
        key = " ".join(dupe.keys()).replace("-", " ").split()
        key = [k.title() for k in key]
        key[0] = key[0].lower()
        key = "".join(key)
        return key

    # Example: flowerShapeLocation
    def add_loc(self, dwc, *args, prepend: str = None) -> None:
        if self.part_location:
            args += ["part", "location"]
            key = self.dwc_key(*args, prepend=prepend)
            dwc.add_dyn(**{key: self.part_location})
