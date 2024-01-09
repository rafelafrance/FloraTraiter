from collections import defaultdict
from dataclasses import asdict
from itertools import product

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc

LINK_TRAITS = "link_traits"

NO_LIMIT = 999_999


# ---------------------
class LinkMatch:
    def __init__(self, span, weights, doc, parents, reverse_weights):
        self.span = span
        self.doc = doc
        self.weights = weights
        self.parents = parents

        child, parent = self.span.start, self.span.end - 1
        if self.span[0].ent_type_ in self.parents:
            child, parent = parent, child

        self.child_ent = self.get_ent_from_token(child)
        self.parent_ent = self.get_ent_from_token(parent)

        self.child_idx = self.child_ent.start
        self.parent_idx = self.parent_ent.start

        self.child_trait = self.child_ent._.trait.trait
        self.parent_trait = self.parent_ent._.trait.trait
        self.reverse_weights = reverse_weights
        self.distance = self.weighted_distance()

    def __lt__(self, other):
        return self.distance < other.distance

    def __len__(self):
        return len(self.span)

    def get_ent_from_token(self, token_idx):
        return next(e for e in self.doc.ents if e.start <= token_idx < e.end)

    def get_inner_indexes(self):
        if self.parent_idx < self.child_idx:
            start, end = self.parent_ent.end, self.child_ent.start
        else:
            start, end = self.child_ent.end, self.parent_ent.start
        return start, end

    def weighted_distance(self):
        """
        Calculate the weighted distance between the parent and child.

        Weights may differ if the parent or child comes first in the doc.
        If the parent comes before the child it's forwards.

        Weight:
            Each entity counts as 1
            Each token value is looked up in the weights table and that value is added
        """
        # Are we counting tokens weights forwards or backwards
        weights = self.weights
        if self.parent_idx > self.child_idx:
            weights = self.reverse_weights

        distance = 0
        start, end = self.get_inner_indexes()

        # Count entities inbetween the parent and child
        ent_indexes = set()
        for ent in self.span.ents:
            if ent.start >= start and ent.end <= end:
                distance += 1
            ent_indexes |= set(range(ent.start, ent.end))

        # Get token values between the parent and child that are not in entities
        for i in range(start, end):
            if i not in ent_indexes:
                distance += weights.get(self.doc[i].lower_, 1)

        return distance


# ---------------------
class LinkCount:
    """How many times have we seen a parent/child combination."""

    def __init__(self, differ: list[str], max_count: int):
        self.differ = differ
        self.max_count = max_count
        self.seen: dict[tuple, int] = defaultdict(int)

    def products(self, ent):
        values = []
        for d in self.differ:
            v = getattr(ent._.trait, d, None)
            values.append(v if isinstance(v, list | tuple) else [v])

        return product(*values)

    def seen_too_much(self, ent):
        """Check if we've seen this link type (parent to trait) too many times."""
        return any(self.seen[k] >= self.max_count for k in self.products(ent))

    def update_seen(self, ent):
        """Update the already seen values for each field."""
        for key in self.products(ent):
            self.seen[key] += 1


# ---------------------
@Language.factory(LINK_TRAITS)
class LinkTraits:
    def __init__(
        self,
        nlp: Language,
        name: str,
        patterns: list[dict],
        parents: list[str],
        children: list[str],
        weights: dict[str, int] | None = None,  # Token weights for scoring distances
        reverse_weights: dict[str, int] | None = None,  # Weights for scoring backwards
        max_links: int = NO_LIMIT,  # Max times to link to a parent trait
        differ: list[str] | None = None,
    ):
        self.nlp = nlp
        self.name = name
        self.patterns = patterns
        self.parents = parents
        self.parent_set = set(parents)
        self.children = children
        self.weights = {k.lower(): v for k, v in weights.items()} if weights else {}
        self.reverse_weights = (
            {k.lower(): v for k, v in reverse_weights.items()}
            if reverse_weights
            else self.weights
        )
        self.max_links = max_links
        self.differ = differ if differ else []
        self.matcher = self.build_matcher(nlp, patterns)

    @staticmethod
    def build_matcher(nlp, patterns):
        matcher = Matcher(nlp.vocab)
        for pattern in patterns:
            matcher.add(pattern["label"], [pattern["pattern"]])
        return matcher

    def __call__(self, doc: Doc) -> Doc:
        matches = self.matcher(doc, as_spans=True)

        # Filter the matches
        link_matches = {}
        for match in matches:
            link_match = LinkMatch(
                match,
                self.weights,
                doc,
                self.parents,
                self.reverse_weights,
            )
            # Matches work by tokens, but I want to match entities, so I only keep
            # matches by entity and filter excess token matches.
            child_start = link_match.child_ent.start
            parent_start = link_match.parent_ent.start
            link_matches[(child_start, parent_start)] = link_match

        # Sort matches by distance and get rid of no longer needed key
        link_matches = sorted(link_matches.values())

        parent_link_count = defaultdict(lambda: LinkCount(self.differ, self.max_links))

        for match in link_matches:
            # Linking to itself is not allowed
            if len(match) <= 1:
                continue

            # Is the child trait field already linked to another parent
            child_set = {
                k for k, v in asdict(match.child_ent._.trait).items() if v is not None
            }
            if child_set & self.parent_set:
                continue

            # Is the parent's link limit exceeded. For example, we only allow a seed
            # to have one size range but many colors
            link_count = parent_link_count[match.parent_idx, match.child_trait]
            if link_count.seen_too_much(match.child_ent):
                continue
            link_count.update_seen(match.child_ent)

            # Update the child entity
            if hasattr(match.parent_ent._.trait, match.parent_trait):
                parent_value = getattr(match.parent_ent._.trait, match.parent_trait)
                setattr(match.child_ent._.trait, match.parent_trait, parent_value)

        return doc
