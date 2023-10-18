from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add

from .part import PART_LABELS


def build(nlp: Language):
    config = {
        "check": """color count shape size surface location margin""".split(),
        "missing": PART_LABELS + ["subpart", "multiple_parts"],
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
                self.clear_tokens(ent)
                continue

            if ent.label_ in self.check:
                data = ent._.trait.as_dict()
                is_missing = set(data.keys()) & self.missing_set
                if not is_missing:
                    self.clear_tokens(ent)
                    continue

            entities.append(ent)

        doc.ents = entities
        return doc

    @staticmethod
    def clear_tokens(ent):
        for token in ent:
            token._.trait = None
            token._.flag = ""
            token._.term = ""
