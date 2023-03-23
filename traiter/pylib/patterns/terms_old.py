from ..term_list import TermList

COLOR_TERMS = TermList().shared("colors").add_trailing_dash()

DATE_TERMS = TermList().shared("time").pick("month")

ELEV_TERMS = TermList().shared("labels units")

HABITAT_TERMS = TermList().shared("habitat")

LAT_LONG_TERMS = TermList().shared("lat_long units")

FACTORS_CM = ELEV_TERMS.pattern_dict("factor_cm", float)  # Convert inches etc. to cm.
FACTORS_M = {k: v / 100.0 for k, v in FACTORS_CM.items()}  # Convert ft. to meters

ALL_TERMS = COLOR_TERMS + DATE_TERMS + ELEV_TERMS + HABITAT_TERMS + LAT_LONG_TERMS
# ALL_TERMS = DATE_TERMS + ELEV_TERMS + HABITAT_TERMS + LAT_LONG_TERMS

KEEP = """ color date elevation habitat lat_long """.split()