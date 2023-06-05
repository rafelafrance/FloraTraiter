import json
from pathlib import Path

from spacy.language import Language
from spacy.tokens import Doc
from traiter.pylib.pipes import add

from .part import PART_LABELS


def build(nlp: Language):
    config = {
        "check": ["count", "size", "location"],
        "missing": PART_LABELS + ["subpart"],
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
        self.missing = missing if missing else []  # Delete if missing these
        self.missing_set = set(self.missing)

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete:
                self.clear_tokens(ent)
                continue

            if ent.label_ in self.check:
                data = ent._.data
                has_part = set(data.keys()) & self.missing_set
                if not has_part:
                    self.clear_tokens(ent)
                    continue

            entities.append(ent)

        doc.ents = entities
        return doc

    def to_disk(self, path, exclude=tuple()):  # noqa
        path = Path(path)
        if not path.exists():
            path.mkdir()
        data_path = path / "data.json"
        skip = ("nlp", "name", "missing_set")
        fields = {k: v for k, v in self.__dict__.items() if k not in skip}
        with data_path.open("w") as data_file:
            data_file.write(json.dumps(fields))

    def from_disk(self, path, exclude=tuple()):  # noqa
        data_path = Path(path) / "data.json"
        with data_path.open("r", encoding="utf8") as data_file:
            data = json.load(data_file)
            for key in data.keys():
                self.__dict__[key] = data[key]
        self.missing_set = set(self.missing)

    @staticmethod
    def clear_tokens(ent):
        for token in ent:
            token._.data = {}
            token._.flag = ""
            token._.term = ""
