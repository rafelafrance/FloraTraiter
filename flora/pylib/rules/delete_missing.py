from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add

from flora.pylib import trait_util as tu


def pipe(nlp: Language):
    config = {
        "check": """color count shape size surface margin""".split(),
        "missing": ["part", "subpart", "multiple_parts"],
    }
    add.custom_pipe(nlp, "delete_missing", config=config)


@Language.factory("delete_missing")
class DeleteMissing:
    def __init__(
        self,
        nlp: Language,
        name: str,
        check: list[str],
        missing: list[str],
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.check = check if check else []  # List of traits to check
        self.if_missing = missing if missing else []  # Delete if missing these
        self.missing_set = set(self.if_missing)

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete:
                tu.clear_tokens(ent)
                continue

            if ent.label_ in self.check:
                data = ent._.trait.to_dict()
                is_missing = set(data.keys()) & self.missing_set
                if not is_missing:
                    tu.clear_tokens(ent)
                    continue

            entities.append(ent)

        doc.ents = entities
        return doc
