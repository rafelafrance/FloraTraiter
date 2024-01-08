from spacy.tokens import Span
from spacy.util import registry

REJECT_MATCH = "reject_match"


class RejectMatch(Exception):
    """
    Raise this when you want to remove a match from doc.ents.

    If you're processing a match, and you discover that it really isn't a trait/entity
    then you'd raise this exception so the match would not be included in the
    document's entities.
    """


@registry.misc(REJECT_MATCH)
def reject_match(_: Span) -> None:
    """
    Use this to reject a pattern from doc.ents.

    Sometimes it is easier to search for a pattern that you know you don't want
    rather than writing a bunch of rules to work around a set of bad patterns within
    the normal set of rules.
    """
    raise RejectMatch
