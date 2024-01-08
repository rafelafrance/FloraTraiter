from spacy.language import Language
from spacy.tokens import Doc

CLEANUP_TRAITS = "cleanup_traits"


@Language.factory(CLEANUP_TRAITS)
class CleanupTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        keep: list[str] | None = None,  # List of trait labels to keep
        *,
        clear: bool = True,
    ):
        super().__init__()
        self.nlp = nlp
        self.name = name
        self.keep = keep if keep else []
        self.clear = clear

    def __call__(self, doc: Doc) -> Doc:
        entities = []

        for ent in doc.ents:
            if ent._.delete or ent.label_ not in self.keep:
                self.clear_tokens(ent)
                continue

            entities.append(ent)

        doc.set_ents(entities)
        return doc

    def clear_tokens(self, ent):
        if self.clear:
            if "" not in ent.doc.vocab.strings:
                ent.doc.vocab.strings.add("")
            ent.label = ent.doc.vocab.strings[""]
            for token in ent:
                token.ent_type = ent.doc.vocab.strings[""]
                token._.flag = ""
                token._.term = ""
