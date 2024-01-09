"""RuleList for parsing and rule builders."""
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import Any

import regex as re

RE_FLAGS = re.VERBOSE | re.IGNORECASE

TOKEN = 0
SIZE = 4

# Find tokens in the regex. Look for words that are not part of a group
# name or a metacharacter. So, "word" not "<word>". Neither "(?P" nor "\b".
WORD = re.compile(
    r"""
    (?<! \(\?P< ) (?<! \(\? ) (?<! [\\] )
    \b (?P<word> [a-z]\w* ) \b """,
    RE_FLAGS,
)

Rules = list["Rule"]
RuleDict = dict[str, "Rule"]
Groups = dict[str, str | list[str]]
Action = Callable[[Any], Any]  # "Any" squashes linter
InRegexp = str | list[str]

FIRST = -9999
SECOND = -9990
LOWEST = 9999


class RuleType(IntEnum):
    """What type of rule are we dealing with."""

    SCANNER = 1
    GROUPER = 2
    REPLACER = 3
    PRODUCER = 4


@dataclass
class Rule:  # pylint: disable=too-many-instance-attributes
    """Create a rule."""

    name: str  # Unique within a catalog but not across catalogs
    pattern: str  # The regex before it is manipulated
    type: RuleType
    token: str
    action: Action | None = None  # What to do when there is a match
    regexp: re.Pattern | None = None  # The compiled regexp
    capture: bool = True  # Will the rule create an outer capture group?
    priority: int = 0  # When should the rule be triggered: FIRST? LAST?

    def __lt__(self, other: "Rule"):
        """Sort in a custom order."""
        return (self.type, self.priority) < (other.type, other.priority)

    def __eq__(self, other):
        """Compare tokens for tests."""
        fields = ("name", "pattern", "type", "action", "capture", "priority")
        you = tuple(v for k, v in other.__dict__.items() if k in fields)
        me_ = tuple(v for k, v in self.__dict__.items() if k in fields)
        return me_ == you

    def build(self, rules: RuleDict) -> str:
        """Build regular expressions for token matches."""

        def _rep(match):
            word = match.group("word")
            if word not in rules:
                print(f"Error: In '{self.name}', {word}' is not defined.")
            sub = rules.get(word)

            if sub.type == RuleType.SCANNER:
                return rf"(?: {sub.token} )"

            return sub.regexp.pattern

        regexp = WORD.sub(_rep, self.pattern)

        if self.capture:
            return rf"(?P<{self.name}> {regexp} )"
        return rf"(?: {regexp} )"

    def compile(self, rules: RuleDict):
        """Build and compile a rule."""
        pattern = self.build(rules)
        self.regexp = re.compile(pattern, RE_FLAGS)


def next_token() -> str:
    """Get the next token."""
    global TOKEN  # pylint: disable=global-statement
    TOKEN += 1
    return f"{TOKEN:04x}"


def join(regexp: InRegexp) -> str:
    """Build a single regexp from multiple strings."""
    if isinstance(regexp, list | tuple | set):
        regexp = " | ".join(regexp)
    return " ".join(regexp.split())


def part(
    name: str,
    regexp: InRegexp,
    action: Action = None,
    *,
    capture: bool = True,
    priority: int = 0,
) -> Rule:
    """Build a regular expression with a named group."""
    pattern = join(regexp)
    reg_ = f"(?P<{name}> {pattern} )" if capture else f"(?: {pattern} )"
    reg = re.compile(reg_, RE_FLAGS)
    return Rule(
        name=name,
        pattern=pattern,
        type=RuleType.SCANNER,
        token=next_token(),
        action=action,
        regexp=reg,
        priority=priority,
    )


def term(
    name: str,
    regexp: InRegexp,
    action: Action = None,
    *,
    capture: bool = True,
    priority: int = 0,
) -> Rule:
    r"""Wrap a regular expression in \b character classes."""
    pattern = join(regexp)
    reg_ = f"(?P<{name}> {pattern} )" if capture else f"(?: {pattern} )"
    reg = re.compile(rf"\b {reg_} \b", RE_FLAGS)
    return Rule(
        name=name,
        pattern=pattern,
        type=RuleType.SCANNER,
        token=next_token(),
        action=action,
        regexp=reg,
        priority=priority,
    )


def grouper(
    name: str,
    regexp: InRegexp,
    action: Action = None,
    *,
    capture: bool = True,
    priority: int = 0,
) -> Rule:
    """Build a grouper regular expression."""
    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.GROUPER,
        token=next_token(),
        action=action,
        capture=capture,
        priority=priority,
    )


def replacer(
    name: str,
    regexp: InRegexp,
    action: Action = None,
    *,
    capture: bool = True,
    priority: int = 0,
) -> Rule:
    """Build a replacer regular expression."""
    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.REPLACER,
        token=next_token(),
        action=action,
        capture=capture,
        priority=priority,
    )


def producer(
    action: Action,
    regexp: InRegexp,
    name: str | None = None,
    *,
    capture: bool = False,
    priority: int = 0,
) -> Rule:
    """Build a product regular expression."""
    token = next_token()
    name = name if name else f"producer_{token}"

    return Rule(
        name=name,
        pattern=join(regexp),
        type=RuleType.PRODUCER,
        token=token,
        action=action,
        capture=capture,
        priority=priority,
    )
