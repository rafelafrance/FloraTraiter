from pathlib import Path

from traiter.pylib import term_util

from ..traits import terms
from ..traits.part import PART_LABELS

LOCATION_CSV = Path(terms.__file__).parent / "part_location_terms.csv"
LOCATION_ENTS = term_util.get_labels(LOCATION_CSV)

TITLE_SKIPS = ["start", "end"]
FIELD_SKIPS = TITLE_SKIPS + ["trait", "dimensions"]
FIELD_SKIPS += PART_LABELS + ["subpart"]
COLUMN_SKIPS = FIELD_SKIPS + ["taxon"]
TRAIT_SKIPS = PART_LABELS + LOCATION_ENTS + ["subpart", "sex"]

PARTS_SET = set(PART_LABELS)
SUBPART_SET = {"subpart"}


def label_parts(trait):
    keys = set(trait.keys())

    name = {}  # Dicts preserve order sets do not

    part_key = list(keys & PARTS_SET)
    part = trait[part_key[0]] if part_key else ""
    name[" ".join(part) if isinstance(part, list) else part] = 1

    subpart_key = list(keys & SUBPART_SET)
    if subpart_key:
        name[trait[subpart_key[0]]] = 1

    name[trait["trait"]] = 1

    if trait.get("sex"):
        name[trait["sex"]] = 1

    return name


def html_label(trait):
    parts = label_parts(trait)

    parts = "_".join(parts.keys())
    parts = parts.strip().replace(" ", "_").replace("-", "")
    parts = parts.removeprefix("_")
    parts = parts.removesuffix("_part")

    return parts


def dwc_label(trait):
    parts = label_parts(trait)

    parts = " ".join(parts)
    parts = parts.removesuffix("part")
    parts = parts.replace("-", " ")
    parts = parts.title()
    parts = "".join(parts.split())

    return parts
