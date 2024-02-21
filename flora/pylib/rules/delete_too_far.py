from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add


def pipe(nlp: Language):
    config = {
        "radius": 5,
        "targets": ["count"],
        "check": ["_part_dist", "_subpart_dist"],
    }
    add.custom_pipe(nlp, "delete_too_far", config=config)


@Language.factory("delete_too_far")
class DeleteTooFar:
    """Delete target traits when they are too far from their linked traits."""

    def __init__(
        self,
        nlp: Language,
        name: str,
        radius: int,
        targets: list[str],
        check: list[str],
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.radius = radius
        self.targets = targets
        self.check = check

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent.label_ not in self.targets:
                entities.append(ent)
            elif any(getattr(ent._.trait, f) <= self.radius for f in self.check):
                entities.append(ent)

        doc.ents = entities
        return doc
