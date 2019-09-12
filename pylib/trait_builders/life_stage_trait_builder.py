"""Parse life stage notations."""

from pylib.trait_builders.base_trait_builder import BaseTraitBuilder
from pylib.shared_patterns import SharedPatterns


class LifeStageTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        tkn = SharedPatterns()
        time_options = tkn['time_units'].pattern

        # JSON keys for life stage
        self.keyword('json_key', [
            r' life \s* stage \s* (remarks?)? ',
            r' age \s* class ',
            r' age \s* in \s* (?P<time_units> {}) '.format(time_options),
            r' age '])

        # These words are life stages without a keyword indicator
        self.keyword('intrinsic', [
            r' yolk \s? sac ',
            r' young [\s-]? of [\s-]? the [\s-]? year ',
            r' adult \s* young ',
            r' young \s* adult ']
                     + """
                ads? adulte?s?
                chicks?
                fledgelings? fleglings?
                fry
                hatched hatchlings?
                imagos?
                imms? immatures?
                jeunes? juvs? juveniles? juvéniles?
                larvae? larvals? larves?
                leptocephales? leptocephalus
                matures? metamorphs?
                neonates?
                nestlings?
                nulliparous
                premetamorphs?
                sub-adults? subads? subadulte?s?
                tadpoles?
                têtard
                yearlings?
                yg ygs young
            """.split())

        # This indicates that the following words are NOT a life stage
        self.keyword('skip', r' determin \w* ')

        # Compound words separated by dashes or slashes
        # E.g. adult/juvenile or over-winter
        self.fragment('joiner', r' \s* [/-] \s* ')

        # Use this to find the end of a life stage pattern
        self.fragment('separator', r' [;,"?] | $ ')

        # For life stages with numbers as words in them
        self.copy(tkn['ordinals'])

        # Time units
        self.copy(tkn['time_units'])

        # Literals
        self.fragment('after', 'after')
        self.fragment('hatching', 'hatching')

        # Match any word
        self.fragment('word', r' \b \w [\w?./-]* (?! [./-] ) ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace(
            'as_time', '( after )? (ordinals | hatching) time_units')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [

            # E.g.: life stage juvenile/yearling
            'json_key (?P<value> ( intrinsic | word ) joiner intrinsic )',

            # E.g.: life stage young adult
            'json_key (?P<value> ( intrinsic | word ) intrinsic )',

            # E.g.: life stage yearling
            'json_key (?P<value> intrinsic )',

            # A sequence of words bracketed by a keyword and a separator
            # E.g.: LifeStage Remarks: 5-6 wks;
            """json_key (?P<value> ( intrinsic | word | joiner ){1,5} )
                separator""",

            # E.g.: LifeStage = 1st month
            'json_key (?P<value> as_time )',

            # E.g.: Juvenile
            '(?P<value> intrinsic )',

            # E.g.: 1st year
            '(?P<value> as_time )'])
