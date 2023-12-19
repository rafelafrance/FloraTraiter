"""Extract information for further analysis."""
from collections import deque
from typing import List
from typing import Tuple
from typing import Union

from .rule import Groups
from .rule import RuleDict
from .rule import Rules
from .rule import RuleType
from .rule import SIZE
from .token import Token
from .token import Tokens
from .util import flatten

RulesInput = Union[Rules, List[Rules]]


class Parser:
    def __init__(self, rules: RulesInput, name: str = "parser") -> None:
        """Build the parser."""
        self.name: str = name
        self.rules: RuleDict = {}
        self._built = False
        self.scanners: Rules = []
        self.replacers: Rules = []
        self.producers: Rules = []
        self.__add__(rules)

    def __add__(self, rule_list: List[Rules]) -> None:
        """Add rules to the parser."""
        self._built = False
        for rule in sorted(flatten(rule_list)):
            if rule.name in self.rules:
                if rule != self.rules[rule.name]:
                    raise ValueError(f'Redefining "{rule.name}"')
            else:
                self.rules[rule.name] = rule

    def parse(self, text: str) -> Tokens:
        """Extract information from the text."""
        if not self._built:
            self.build()

        tokens = self.scan(text)

        again = bool(self.replacers)
        while again:
            tokens, again = self.replace(tokens, text)

        # for token in tokens:
        #     print(token)
        # print()

        if self.producers:
            tokens = self.produce(tokens, text)

        return tokens

    def build(self) -> None:
        """Build the regular expressions."""
        self._built = True
        self.scanners = [
            r for r in sorted(self.rules.values()) if r.type == RuleType.SCANNER
        ]

        rules = [r for r in sorted(self.rules.values()) if r.type != RuleType.SCANNER]
        for rule in rules:
            rule.compile(self.rules)
            if rule.type == RuleType.PRODUCER:
                self.producers.append(rule)
            elif rule.type == RuleType.REPLACER:
                self.replacers.append(rule)

    def scan(self, text: str) -> Tokens:
        """Scan a string & return tokens."""
        tokens = []
        matches_ = self.get_matches(self.scanners, text)
        matches = self.sort_matches(matches_)

        while matches:
            token = matches.popleft()
            if token.action:
                token.action(token)
            tokens.append(token)
        return tokens

    def produce(self, tokens: Tokens, text: str) -> Tokens:
        """Produce final tokens for consumption by the client code."""
        results = []
        token_text = "".join(t.rule.token for t in tokens if t)
        matches = self.match_tokens(self.producers, token_text)

        while matches:
            match = matches.popleft()
            token, *_ = self.merge_tokens(match, tokens, text)
            results.append(token)

        return results

    @staticmethod
    def get_matches(rules: Rules, text: str) -> Tokens:
        """Get all the text matches for the rules sorted by position."""
        pairs = [(r, r.regexp.finditer(text)) for r in rules]
        return [Token(match[0], match=m) for match in pairs for m in match[1]]

    def sort_matches(self, tokens: Tokens) -> deque:
        """Sort the matches by starting span and when and then by longest."""
        matches = deque(
            sorted(tokens, key=lambda m: (m.span[0], m.rule.priority, -m.span[1]))
        )
        matches = self.remove_overlapping(matches)
        return matches

    def match_tokens(self, rules: Rules, text: str) -> deque:
        """Get all the token matches for the rules sorted by position."""
        matches = self.get_matches(rules, text)
        matches = [t for t in matches if t.valid_match()]
        return self.sort_matches(matches)

    @staticmethod
    def remove_overlapping(matches: deque) -> deque:
        """Remove matches that overlap a previous match."""
        cleaned: deque = deque()
        while matches:
            cleaned.append(matches.popleft())
            while matches and matches[0].span[0] < cleaned[-1].span[1]:
                matches.popleft()
        return cleaned

    @staticmethod
    def append_group(groups: Groups, key: str, value: str) -> None:
        """Append a group to the groups' dictionary."""
        old: list[str] = []
        if key in groups:
            old = groups[key] if isinstance(groups[key], list) else [groups[key]]
        new = value if isinstance(value, list) else [value]
        values = old + new
        groups[key] = values[0] if len(values) == 1 else values

    def merge_tokens(
        self, match: Token, tokens: Tokens, text: str
    ) -> Tuple[Token, int, int]:
        """Merge all matched tokens into one token."""
        # Get tokens in match
        first_idx = match.start // SIZE
        last_idx = match.end // SIZE
        span = (tokens[first_idx].start, tokens[last_idx - 1].end)

        # Merge all subgroups from sub-tokens into current token
        groups = {}
        for token in tokens[first_idx:last_idx]:
            for key, value in token.group.items():
                self.append_group(groups, key, value)

        # Add groups from current token with real (not tokenized) text
        for key in match.match.capturesdict():
            for i, value in enumerate(match.match.captures(key)):
                idx1 = match.match.starts(key)[i] // SIZE
                idx2 = match.match.ends(key)[i] // SIZE - 1
                self.append_group(
                    groups, key, text[tokens[idx1].start : tokens[idx2].end]
                )

        token = Token(match.rule, span=span, group=groups)
        return token, first_idx, last_idx

    def replace(self, tokens: Tokens, text: str) -> Tuple[Tokens, bool]:
        """Replace token combinations with another token."""
        replaced = []
        token_text = "".join([t.rule.token for t in tokens])
        matches = self.match_tokens(self.replacers, token_text)
        again = bool(matches)

        prev_idx = 0
        while matches:
            match = matches.popleft()
            token, first_idx, last_idx = self.merge_tokens(match, tokens, text)
            if token.action:
                token.action(token)
            if prev_idx != first_idx:
                replaced += tokens[prev_idx:first_idx]
            replaced.append(token)
            prev_idx = last_idx

        if prev_idx != len(tokens):
            replaced += tokens[prev_idx:]

        return replaced, again
