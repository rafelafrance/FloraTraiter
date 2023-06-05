from pathlib import Path

from traiter.pylib import term_util

from plants.pylib.traits import terms
from plants.pylib.traits.part import PART_LABELS

LOCATION_CSV = Path(terms.__file__).parent / "part_location_terms.csv"
LOCATION_ENTS = term_util.get_labels(LOCATION_CSV)

TITLE_SKIPS = ["start", "end"]
FIELD_SKIPS = TITLE_SKIPS + ["trait", "dimensions"]
FIELD_SKIPS += PART_LABELS + ["subpart"]
COLUMN_SKIPS = FIELD_SKIPS + ["taxon"]
TRAIT_SKIPS = PART_LABELS + LOCATION_ENTS + ["subpart", "sex"]

PARTS_SET = set(PART_LABELS)
SUBPART_SET = {"subpart"}


def get_label(trait):
    keys = set(trait.keys())

    label = {}  # Dicts preserve order sets do not

    part_key = list(keys & PARTS_SET)
    part = trait[part_key[0]] if part_key else ""
    label[" ".join(part) if isinstance(part, list) else part] = 1

    subpart_key = list(keys & SUBPART_SET)
    if subpart_key:
        label[trait[subpart_key[0]]] = 1

    label[trait["trait"]] = 1

    if trait.get("sex"):
        label[trait["sex"]] = 1

    label = "_".join(label.keys())
    label = label.strip().replace(" ", "_").replace("-", "")
    label = label.removeprefix("_")
    label = label.removesuffix("_part")

    return label
