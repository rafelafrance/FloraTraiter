from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add


def pipe(nlp: Language):
    add.custom_pipe(nlp, "flora_post_process")


@Language.factory("flora_post_process")
class FloraPostProcess:
    def __init__(self, nlp: Language, name: str):
        super().__init__()
        self.nlp = nlp
        self.name = name

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ == "name":
                continue

            entities.append(ent)

        entities.reverse()
        doc.ents = entities
        return doc
