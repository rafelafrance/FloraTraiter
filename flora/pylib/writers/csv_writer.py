import sys
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

import pandas as pd
from traiter.pylib.darwin_core import DarwinCore

from flora.pylib.treatments import Treatments

TAXON = "dwc:scientificName"
FIRST = ["taxon", "treatment"]


def write_csv(treatments: Treatments, csv_file: Path):
    rows = []
    for treatment in treatments:
        grouped = group_traits(treatment)
        flattened = flatten_traits(grouped)
        formatted = remove_duplicates(flattened)
        add_row_fields(treatment, formatted)
        rows.append(formatted)

    max_indexes = get_max_indexes(rows)
    rows = number_columns(rows, max_indexes)

    df = pd.DataFrame(rows)

    columns = FIRST
    columns += sorted(c for c in df.columns if c not in FIRST)
    df = df[columns]

    df = df.sort_values(by="taxon")

    df.to_csv(csv_file, index=False)


def number_columns(rows, max_indexes):
    new_rows = []
    for row in rows:
        new_row = {}
        for (key, i), value in row.items():
            use_index = max_indexes[key] > 1
            for col, val in value.items():
                parts = col.split("_")
                if use_index:
                    parts.insert(1, str(i))
                name = "_".join(parts)

                new_row[name] = val

        new_rows.append(new_row)
    return new_rows


def get_max_indexes(rows):
    max_index = defaultdict(int)
    for row in rows:
        for key, i in row:
            max_index[key] = max(i, max_index[key])
    return max_index


def remove_duplicates(flattened):
    cleaned = {}
    for key, values in flattened.items():
        i = 0
        used = set()
        for val in values:
            as_tuple = tuple((k, to_hashable(v)) for k, v in val.items())
            if as_tuple not in used:
                i += 1
                used.add(as_tuple)
                cleaned[(key, i)] = val
    return cleaned


def add_row_fields(treatment, formatted: dict[tuple, dict]) -> None:
    taxon = formatted.get((TAXON, 1))
    taxon = taxon[TAXON] if taxon else "unknown"
    formatted[("taxon", 1)] = {"taxon": taxon}
    formatted[("treatment", 1)] = {"treatment": treatment.path.stem}


def group_traits(treatment) -> dict[str, list[DarwinCore]]:
    grouped: dict[str, list[DarwinCore]] = defaultdict(list)
    for trait in treatment.traits:
        dwc = DarwinCore()
        dwc_trait = trait.to_dwc(dwc)
        grouped[trait.key].append(dwc_trait)
    return grouped


def flatten_traits(grouped) -> dict[str, list]:
    flattened = defaultdict(list)
    for name, dwc_list in grouped.items():
        for dwc_value in dwc_list:
            new = {}
            flat = dwc_value.flatten()
            for key, value in flat.items():
                if isinstance(value, dict):
                    for field, val in value.items():
                        new[f"{key}_{field}"] = val
                else:
                    new[key] = value
            flattened[name].append(new)
    return flattened


def to_hashable(val):
    if isinstance(val, dict):
        return tuple(val.items())
    if isinstance(val, Iterable):
        return tuple(val)
    try:
        hash(val)
    except TypeError:
        sys.exit(f"Could not hash '{val}'")
    return val
