from dataclasses import dataclass

from spacy.language import Language


@dataclass
class Linker:
    @classmethod
    def pipe(cls, nlp: Language):
        raise NotImplementedError
