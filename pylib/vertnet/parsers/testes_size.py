"""Parse testes size notations."""

from pylib.stacked_regex.rule import fragment, keyword, producer, grouper
from pylib.vertnet.shared_reproductive_patterns import RULE
from pylib.vertnet.parsers.reproductive import double, convert
from pylib.vertnet.parsers.base import Base


TESTES_SIZE = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['testes'],

        # Note: abbrev differs from the one in the testes_state_trait
        keyword('abbrev', 'tes ts tnd td tns ta'.split()),

        # The abbreviation key, just: t. This can be a problem.
        fragment('char_key', r' \b t (?! [a-z] )'),

        RULE['descended'],
        RULE['scrotal'],
        RULE['abdominal'],
        RULE['size'],
        RULE['other'],

        RULE['uuid'],  # UUIDs cause problems with numeric traits

        RULE['label'],
        RULE['ambiguous_key'],
        RULE['non'],
        RULE['fully'],
        RULE['partially'],
        RULE['side_cross'],
        RULE['side'],
        RULE['dim_side'],
        RULE['dimension'],
        RULE['cross'],
        RULE['len_units'],
        RULE['in'],
        RULE['word'],
        RULE['sep'],

        grouper('state', [
            """(non | partially | fully )? descended """]
                 + """ scrotal abdominal size other """.split()),

        # A key with units, like: gonadLengthInMM
        grouper('key_with_units', r"""
            ambiguous_key dimension in (?P<units> len_units )
            """),

        # Male or female ambiguous, like: gonadLength1
        grouper('ambiguous', [
            # E.g.: GonadWidth2
            r' ambiguous_key dim_side',

            # E.g.: LeftGonadLength
            r' side ambiguous_key dimension ',

            # E.g.: Gonad Length
            r' ambiguous_key dimension ']),

        # These patterns contain measurements to both left & right testes
        # E.g.: reproductive data: tests left 10x5 mm, right 10x6 mm
        producer(
            double, """label ( testes | abbrev | char_key ) side_cross """),

        # As above but without the testes marker:
        # E.g.: reproductive data: left 10x5 mm, right 10x6 mm
        producer(double, """ label side_cross """),

        # Has the testes marker but is lacking the label
        # E.g.: testes left 10x5 mm, right 10x6 mm
        producer(double, """( testes | abbrev | char_key ) side_cross """),

        # A typical testes size notation
        # E.g.: reproductive data: tests 10x5 mm
        producer(convert, 'label ( testes | abbrev | char_key ) side_cross'),

        # E.g.: reproductive data: left tests 10x5 mm
        producer(convert, 'label side ( testes | abbrev | char_key ) cross'),

        # E.g.: reproductive data=T: L-2x4mm
        producer(convert, 'label ( testes | abbrev | char_key ) side cross'),

        # E.g.: reproductive data: 10x5 left mm
        producer(convert, 'label side cross'),

        # E.g.: reproductive data: 10x5 mm
        producer(convert, 'label cross'),

        # Has the testes marker but is lacking the label
        # E.g.: testes left 10x5 mm, right 10x6 mm
        producer(convert, """( testes | abbrev ) cross """),

        # May have a few words between the label and the measurement
        # E.g.: reproductive data=testes not descended - 6 mm
        producer(convert, [
            """label ( testes | abbrev | state | word | sep | char_key){0,3}
                ( testes | abbrev | state | char_key ) cross"""]),

        # Handles: gonadLengthInMM 4x3
        # And:     gonadLength 4x3
        producer(convert, '( key_with_units | ambiguous ) cross'),

        # E.g.: gonadLengthInMM 6 x 8
        producer(convert, [
            """( key_with_units | ambiguous )
                ( testes | abbrev | state | word | sep | char_key ){0,3}
                ( testes | abbrev | state | char_key ) cross"""]),

        # Anchored by testes but with words between
        # E.g.: testes scrotal; T = 9mm
        producer(convert, [
            """testes ( abbrev | state | word | sep | char_key ){0,3}
                ( abbrev | state | char_key ) cross"""]),

        # Anchored by testes but with only one word in between
        # E.g.: testes scrotal 9mm
        producer(convert, 'testes ( abbrev | state | word | char_key ) cross'),

        # E.g.: Testes 5 x 3
        producer(convert, '( testes | state | abbrev ) cross'),

        # E.g.: T 5 x 4
        producer(convert, '(?P<ambiguous_char> char_key ) cross'),
    ],
)
