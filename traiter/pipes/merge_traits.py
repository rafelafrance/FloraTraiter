"""Merge entities into a single token.

This is a wrapper around the spacy merge_entities function that takes into
account merging the entity data before merging the entities themselves.
"""
from spacy.language import Language
from spacy.pipeline.functions import merge_entities
from spacy.tokens import Doc

from traiter.pipes import pipe_util

MERGE_TRAITS = "traiter.merge_traits.v1"


@Language.factory(MERGE_TRAITS)
class MergeTraits:
    def __init__(self, nlp: Language, name: str):
        pipe_util.add_extensions()
        super().__init__()
        self.nlp = nlp
        self.name = name

    def __call__(self, doc: Doc) -> Doc:
        for span in doc.ents:
            for sub_ent in span.ents:
                span[0]._.data |= sub_ent._.data

        doc = merge_entities(doc)
        return doc
