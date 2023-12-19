from spacy.language import Language

MERGE_SELECTED = "merge_selected"


@Language.factory(MERGE_SELECTED)
class MergeSelected:
    def __init__(self, nlp: Language, name: str, labels: list[str]):
        self.nlp = nlp
        self.name = name
        self.labels = labels

    def __call__(self, doc):
        with doc.retokenize() as retokenizer:
            for ent in [e for e in doc.ents if e.label_ in self.labels]:
                attrs = {
                    "ENT_TYPE": ent.label_,
                    "ENT_IOB": 3,
                    "POS": ent.root.pos_,
                    "_": {"trait": ent._.trait},
                }
                retokenizer.merge(ent, attrs=attrs)
        return doc
