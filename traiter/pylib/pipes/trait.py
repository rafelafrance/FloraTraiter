from typing import Any

from spacy import util
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

from traiter.pylib.pipes.reject_match import RejectMatch

ADD_TRAITS = "add_traits"


@Language.factory(ADD_TRAITS)
class AddTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        patterns: dict[str, list[list[dict[str, Any]]]],
        dispatch: dict[str, str] | None = None,
        keep: list[str] | None = None,  # Don't overwrite these entities
        overwrite: list[str] | None = None,  # Only overwrite these entities
        relabel: dict[str, str] | None = None,
    ):
        self.nlp = nlp
        self.name = name
        self.patterns = patterns
        self.dispatch = dispatch
        self.keep = keep if keep else []
        self.overwrite = overwrite if overwrite else []
        self.relabel = relabel if relabel else {}

        self.dispatch_table = self.build_dispatch_table()
        self.matcher = self.build_matcher()

    def build_dispatch_table(self):
        dispatch_table = {}
        if self.dispatch:
            for label, registered in self.dispatch.items():
                if func := util.registry.misc.get(registered):
                    dispatch_table[label] = func
        return dispatch_table

    def build_matcher(self):
        matcher = Matcher(self.nlp.vocab)
        # Can't be greedy if we are keeping traits in the middle of a match
        greedy = None if self.keep else "LONGEST"
        for label, patterns in self.patterns.items():
            matcher.add(label, patterns, greedy=greedy)
        return matcher

    def __call__(self, doc: Doc) -> Doc:
        matches = self.matcher(doc, as_spans=True)

        entities, used_tokens = self.filter_entities(doc)

        matches = self.remove_overlapping_matches(matches, used_tokens)
        matches = util.filter_spans(matches)

        for ent in matches:
            label = ent.label_

            ent_tokens = set(range(ent.start, ent.end))
            if ent_tokens & used_tokens:
                continue

            if action := self.dispatch_table.get(label):
                try:
                    ent._.trait = action(ent)
                except RejectMatch:
                    continue

            used_tokens |= ent_tokens

            self.relabel_ent(ent, label)

            entities.append(ent)

        self.add_untouched_entities(doc, entities, used_tokens)

        doc.set_ents(sorted(entities, key=lambda e: e.start))
        return doc

    @staticmethod
    def add_untouched_entities(doc, entities, used_tokens):
        """Add entities that do not overlap with any of the matches."""
        for ent in doc.ents:
            ent_tokens = set(range(ent.start, ent.end))
            if not ent_tokens & used_tokens:
                entities.append(ent)

    @staticmethod
    def remove_overlapping_matches(matches, used_tokens):
        """Remove any matches that overlap with an entity we kept."""
        filtered_matches = []
        for match in matches:
            ent_tokens = set(range(match.start, match.end))
            if ent_tokens & used_tokens:
                continue
            filtered_matches.append(match)
        return filtered_matches

    def filter_entities(self, doc):
        used_tokens: set[Any] = set()
        entities = []
        for ent in doc.ents:
            if ent.label_ in self.overwrite or ent.label_ not in self.keep:
                continue
            if ent.label_ in self.keep:
                ent_tokens = set(range(ent.start, ent.end))
                used_tokens |= ent_tokens
                entities.append(ent)
        return entities, used_tokens

    def relabel_ent(self, ent, old_label):
        label = old_label

        new_label = self.relabel.get(old_label)
        new_label = ent._.relabel if ent._.relabel else new_label
        if new_label:
            relabel_entity(ent, new_label)
            label = new_label
            ent._.trait.trait = new_label

        return label


def relabel_entity(ent, new_label, *, relabel_tokens=False):
    if new_label not in ent.doc.vocab.strings:
        ent.doc.vocab.strings.add(new_label)
    ent.label = ent.doc.vocab.strings[new_label]
    if relabel_tokens:
        for token in ent:
            token.ent_type = ent.doc.vocab.strings[new_label]
