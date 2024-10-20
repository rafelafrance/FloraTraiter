#!/usr/bin/env python3
"""
Check if data in the CSV and HTML output files, are actually different, as claimed.

Take output files and count the output fields. This may require counting the data at
different levels. If it is different, then figure out why.
"""
import argparse
import csv
import textwrap
from pathlib import Path

from bs4 import BeautifulSoup


def main():
    args = parse_args()

    html_treatments = get_html_treatments(args.html_file)
    csv_treatments = get_csv_treatments(args.csv_file)
    compare_results(html_treatments, csv_treatments)


def get_html_treatments(html_file) -> dict:
    with html_file.open("rb") as in_file:
        raw = in_file.read()

    soup = BeautifulSoup(raw, features="lxml")

    treatments = {}
    treatment = ""
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if "first" in tr.get("class", ""):
            treatment = tds[1].text
        elif "term" in tr.get("class", ""):
            label = tds[1].text
            label = label.split(":")[-1]
            if label not in ("Treatment Label",):
                treatments[(treatment, label)] = 1

    return treatments


def get_csv_treatments(csv_file) -> dict:
    treatments = {}
    with csv_file.open("r") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            treatment = row["treatment"]
            for key, value in row.items():
                if key in ("treatment", "taxon"):
                    continue
                if value not in ("", None):
                    label = key.split("_")[0]
                    label = label.split(":")[-1]
                    if label not in ("scientificNameAuthorship", "taxonRank"):
                        treatments[(treatment, label)] = 1

    return treatments


def compare_results(html_treatments, csv_treatments):
    html_treatments = set(html_treatments.keys())
    csv_treatments = set(csv_treatments.keys())

    disjoint = html_treatments ^ csv_treatments
    for item in sorted(disjoint):
        print("disjoint", item)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """Count traits in output files.""",
        ),
    )

    arg_parser.add_argument(
        "--html-file",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output HTML formatted results to this file.""",
    )

    arg_parser.add_argument(
        "--csv-file",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output results to this CSV file.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
