from dataclasses import asdict, dataclass

from spacy.language import Language

from traiter.pylib.darwin_core import DarwinCore


@dataclass(eq=False)
class Base:
    trait: str = None
    start: int = None
    end: int = None
    _text: str = None

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    @classmethod
    def from_ent(cls, ent, **kwargs):
        kwargs["trait"] = ent.label_
        kwargs["start"] = ent.start_char
        kwargs["end"] = ent.end_char
        kwargs["_text"] = ent.text
        return cls(**kwargs)

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None and k[0] != "_"}

    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError

    def to_dwc(self, dwc) -> DarwinCore:
        raise NotImplementedError

    @staticmethod
    def key_builder(*args, prepend: str | None = None) -> str:
        key = [prepend] if prepend else []
        key += list(args)
        key = " ".join(key).replace("-", " ").split()
        key = [k.title() for k in key]
        key[0] = key[0].lower()
        return "".join(key)

    @property
    def key(self):
        k = self.key_builder(*self.trait.split("_"))
        return DarwinCore.ns(k)
