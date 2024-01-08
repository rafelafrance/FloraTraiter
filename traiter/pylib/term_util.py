import csv
from collections.abc import Iterable
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from zipfile import ZipFile


def term_data(
    csv_path: Path | Iterable[Path],
    field: str,
    type_=None,
) -> dict[str, Any]:
    paths = csv_path if isinstance(csv_path, Iterable) else [csv_path]
    type_ = type_ if type_ else str
    data = {}
    for path in paths:
        terms = read_terms(path)
        for term in terms:
            value = term.get(field)
            if value not in (None, ""):
                data[term["pattern"]] = type_(value)
    return data


def get_labels(
    csv_paths: Path | Iterable[Path],
    default_labels: dict[str, str] | None = None,
) -> list[str]:
    csv_paths = csv_paths if isinstance(csv_paths, Iterable) else [csv_paths]
    default_labels = default_labels if default_labels else {}
    labels = set()
    for path in csv_paths:
        terms = read_terms(path)
        try:
            labels |= {t["label"] for t in terms}
        except KeyError:
            if label := default_labels.get(path.stem):
                labels.add(label)
    return sorted(labels)


def labels_to_remove(
    csv_paths: Path | Iterable[Path],
    *,
    keep: str | Iterable[str] | None = None,
) -> list[str]:
    labels = get_labels(csv_paths)
    if keep:
        keep = keep if isinstance(keep, Iterable) else [keep]
        labels = [lb for lb in labels if lb not in keep]
    return labels


def read_terms(csv_path: Path | Iterable[Path]) -> list[dict]:
    paths = csv_path if isinstance(csv_path, Iterable) else [csv_path]
    terms = []
    for path in paths:
        if path.suffix == ".zip":
            with ZipFile(path) as zippy, zippy.open(f"{path.stem}.csv") as in_csv:
                reader = csv.DictReader(TextIOWrapper(in_csv, "utf-8"))
                terms += list(reader)
        else:
            with path.open() as term_file:
                reader = csv.DictReader(term_file)
                terms += list(reader)
    return terms
