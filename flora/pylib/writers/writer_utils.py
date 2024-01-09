from pathlib import Path

from traiter.pylib import term_util

from flora.pylib.rules import terms

LOCATION_CSV = Path(terms.__file__).parent / "part_location_terms.csv"
LOCATION_ENTS = term_util.get_labels(LOCATION_CSV)

TITLE_SKIPS = ["start", "end"]
FIELD_SKIPS = [*TITLE_SKIPS, "trait", "dimensions"]
FIELD_SKIPS += ["part", "subpart"]
COLUMN_SKIPS = [*FIELD_SKIPS, "taxon"]
TRAIT_SKIPS = [*LOCATION_ENTS, "part", "subpart", "sex"]

SUBPART_SET = {"subpart"}


def label_parts(trait):
    # keys = set(trait.keys())

    name = {}  # Dicts preserve order sets do not

    part = trait.get("part", "")
    name[" ".join(part) if isinstance(part, list) else part] = 1

    subpart = trait.get("subpart", "")
    if subpart:
        name[trait[subpart[0]]] = 1

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
