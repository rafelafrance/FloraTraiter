from .. import term_reader

COLOR_TERMS = term_reader.shared("colors")
COLOR_REPLACE = term_reader.pattern_dict(COLOR_TERMS, "replace")
COLOR_REMOVE = term_reader.pattern_dict(COLOR_TERMS, "remove")

UNIT_TERMS = term_reader.shared("units")
UNIT_FACTORS = term_reader.pattern_dict(UNIT_TERMS, "factor", float)

HABITAT_TERMS = term_reader.shared("habitat")
HABITAT_REPLACE = term_reader.pattern_dict(HABITAT_TERMS, "replace")

PARTIAL_TRAITS = """ habitat_prefix habitat_suffix """.split()
