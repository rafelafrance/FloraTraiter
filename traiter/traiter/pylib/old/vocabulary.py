"""Build catalogs of rules and their parts for sharing."""
from itertools import groupby

from . import rule as re_rule
from .rule import Action, InRegexp, Rule, Rules, grouper, part, producer, replacer, term
from .util import flatten

FIRST = re_rule.FIRST
SECOND = re_rule.SECOND
LOWEST = re_rule.LOWEST


class Vocabulary:
    """
    Build a catalog of shared rules and what sub-patterns they need.

    The purpose of this object is to build a parts list of all patterns so that
    when we pull in one pattern we also automatically pull in all of its
    subordinate patterns without having to remember what they all are. For
    instance, if we have a grouper pattern like:

        grouper('value', ' len_range | number (?P<units> len_units )? ')

    We want to add a rule for the new 'value' grouper, but we also want to make
    sure the 'len_range', 'number', and 'len_units' forms are also included.
    This is done recursively so, for example, the 'len_units' sub-grouper will
    also pull in the 'feet', 'inches', and 'metric_len' basal patterns.

    It is primarily used with shared patterns. We have catalogs of 100s of
    shared patterns, and we only want to pull in (and search through) the ones that
    are needed for a particular product.
    """

    def __init__(self, other=None) -> None:
        """Create the rule set."""
        self.rules: dict = dict(other.rules) if other else {}

    def __getitem__(self, name: str) -> Rule:
        """Emulate dict access of the rules."""
        rule = self.rules[name]
        if isinstance(rule, list):
            return next(r for r in rule if r.name == name)
        return rule

    def part(
        self,
        name: str,
        regexp: InRegexp,
        *,
        capture: bool = True,
        priority: int = 0,
    ) -> Rules:
        """Add a partial term rule."""
        self.rules[name] = part(name, regexp, capture=capture, priority=priority)
        return self.rules[name]

    def term(
        self,
        name: str,
        regexp: InRegexp,
        *,
        capture: bool = True,
        priority: int = 0,
    ) -> Rules:
        """Add a vocabulary term."""
        self.rules[name] = term(name, regexp, capture=capture, priority=priority)
        return self.rules[name]

    def grouper(
        self,
        name: str,
        regexp: InRegexp,
        *,
        capture: bool = True,
        priority: int = 0,
    ) -> Rules:
        """Add a grouper rule."""
        rule = grouper(name, regexp, capture=capture, priority=priority)
        self.rules[name] = self._get_sub_patterns(rule)
        return self.rules[name]

    def replacer(
        self,
        name: str,
        regexp: InRegexp,
        *,
        capture: bool = True,
        priority: int = 0,
    ) -> Rules:
        """Add a replacer rule."""
        rule = replacer(name, regexp, capture=capture, priority=priority)
        self.rules[name] = self._get_sub_patterns(rule)
        return self.rules[name]

    # pylint: disable=too-many-arguments
    def producer(
        self,
        action: Action,
        regexp: InRegexp,
        name: str | None = None,
        *,
        capture: bool = True,
        priority: int = 0,
    ) -> Rules:
        """Add a producer rule."""
        rule = producer(action, regexp, name=name, capture=capture, priority=priority)
        self.rules[rule.name] = self._get_sub_patterns(rule)
        return self.rules[rule.name]

    def _get_sub_patterns(self, rule: Rule) -> Rules:
        rules = [self.rules[w] for w in re_rule.WORD.findall(rule.pattern)]
        rules = flatten(rules)
        rules = sorted(rules)
        rules.append(rule)
        return [next(iter(g)) for _, g in groupby(rules, key=lambda r: r.name)]
