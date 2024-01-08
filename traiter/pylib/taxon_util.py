"""
Taxa are terms (see term_list.py) with 2 types of terms: binomials and monomials.

Taxon traits are build up from these two as well as other terms like ranks and names.
"""
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from traiter.pylib import term_util


def abbreviate_binomials(binomials: list[dict], *, single_expanded_name=True):
    """
    Create a mapping from binomial terms to abbreviated binomials.

    Example: "C. lupus"  -> {"Canis lupus", "Cartoonus lupus"}
         or: "D. Duckus" -> {"Daffyus Duckus"}

    single_expanded_name prunes this mapping to only mappings with a single expanded
    name. So, in the example above only "D. Duckus" would be returned.
    """
    abbrevs = defaultdict(set)

    for term in binomials:
        pattern = term["pattern"]
        abbrev = abbreviate(pattern)
        abbrevs[abbrev].add(pattern.split()[0])

    if single_expanded_name:
        abbrevs = {k: v.pop().title() for k, v in abbrevs.items() if len(v) == 1}

    return abbrevs


def abbrev_binomial_term(csv_path: Path | Iterable[Path]):
    terms = term_util.read_terms(csv_path)
    return abbreviate_binomials(terms)


def abbreviate(pattern):
    genus, *parts = pattern.split()
    abbrev = genus[0].upper() + "."
    return " ".join([abbrev, *parts])
