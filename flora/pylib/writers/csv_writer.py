from collections import defaultdict

import pandas as pd
from traiter.pylib.darwin_core import DarwinCore

from flora.pylib.treatments import Treatments

TAXON = "dwc:scientificName"


def write_csv(treatments: Treatments):
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
    print(df.head())
    # sort columns
    # output data frame


def number_columns(rows, max_indexes):
    new_rows = []
    for row in rows:
        new_row = {}
        for (key, i), value in row.items():
            suffix = f"_{i}" if max_indexes[key] > 1 else ""
            for col, val in value.items():
                new_row[col + suffix] = val

        new_rows.append(new_row)
    return new_rows


def get_max_indexes(rows):
    max_index = defaultdict(int)
    for row in rows:
        for key, i in row:
            if i > max_index[key]:
                max_index[key] = i
    return max_index


def remove_duplicates(flattened):
    cleaned = {}
    for key, values in flattened.items():
        i = 0
        used = set()
        for val in values:
            as_tuple = tuple(val.items())
            if as_tuple not in used:
                i += 1
                used.add(as_tuple)
                cleaned[(key, i)] = val
    return cleaned


def flatten_traits(grouped):
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


def group_traits(treatment):
    grouped: dict[str, list[DarwinCore]] = defaultdict(list)
    for trait in treatment.traits:
        dwc = DarwinCore()
        dwc_trait = trait.to_dwc(dwc)
        grouped[trait.key].append(dwc_trait)
    return grouped


def add_row_fields(treatment, formatted: dict[tuple, dict]):
    taxon = formatted.get((TAXON, 1))
    taxon = taxon[TAXON] if taxon else "unknown"
    formatted[("taxon", 1)] = {"taxon": taxon}
    formatted[("treatment", 1)] = {"treatment": treatment.path.stem}
