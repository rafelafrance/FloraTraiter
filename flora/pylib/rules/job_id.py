"""Only keep unlabeled job or id_number traits if they are near to each other."""

from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add

from flora.pylib import trait_util as tu


def pipe(nlp: Language):
    config = {
        "check": """job id_number""".split(),
        "near": """job id_number date""".split(),
        "radius": 2,  # Keep the entities if they are this close
    }
    add.custom_pipe(nlp, "job_id", config=config)


@Language.factory("job_id")
class JobId:
    def __init__(
        self,
        nlp: Language,
        name: str,
        check: list[str],
        near: list[str],
        radius: int,
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.check = set(check)  # List of traits to check
        self.near = set(near)  # List of traits to be near to
        self.radius = radius  # They must be this close

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for i, ent in enumerate(doc.ents):
            if ent._.delete:
                tu.clear_tokens(ent)
                continue

            if ent.label_ not in self.check or ent._.trait.has_label:
                entities.append(ent)
                continue

            beg = max(0, i - self.radius)
            end = min(len(doc.ents), i + self.radius + 1)

            labels = {lb for k in range(beg, end) if (lb := doc.ents[k].label_)}
            labels &= self.near
            labels -= {ent.label_}

            if labels:
                entities.append(ent)
                continue

            tu.clear_tokens(ent)

        doc.ents = entities
        return doc
