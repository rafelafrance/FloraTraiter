"""Common logic for parsing trait notations."""

import re
from stacked_regex.stacked_regex import StackedRegex
from traiter.util import ordinal


class BaseTraitBuilder(StackedRegex):
    """Shared lexer logic."""

    flags = re.VERBOSE | re.IGNORECASE

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__()

        self.args = args
        self.shared_token = self.from_tuple

    def parse(self, text, field=''):
        """Find the trait_builders in the text.

        We get the trait list from the StackedRegex engine & then fix them up
        afterwards.
        """
        traits = []

        for token in self.match(text):

            trait_list = self.regexps[token.name].action(token)

            # The action function can reject the token
            if not trait_list:
                continue

            # Some parses represent multiple trait_builders, fix them all up
            if not isinstance(trait_list, list):
                trait_list = [trait_list]

            # Add the traits after any fix up.
            for trait in trait_list:
                trait = self.fix_problem_parses(trait, text)
                if trait:
                    trait.field = field
                    traits.append(trait)

        return traits

    def fix_problem_parses(self, trait, text):
        """Fix problematic parses."""
        return trait

    @staticmethod
    def csv_formatter(trait_name, row, traits):
        """Format the trait for CSV output."""
        records = {}
        for trait in traits:
            key = trait.as_key()
            if key not in records:
                records[key] = trait

        for i, trait in enumerate(records.values(), 1):
            row[f'{trait_name}:{ordinal(i)}_{trait_name}_notation'] = \
                trait.value

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        return False

    @staticmethod
    def adjust_record(data, trait):
        """Adjust the trait based on other fields."""
