#!/usr/bin/env python3
import argparse
import sys
import textwrap
from pathlib import Path

from pylib import pipeline

from efloras.pylib.readers import efloras_reader as reader
from efloras.pylib.writers.csv_writer import CsvWriter
from efloras.pylib.writers.html_writer import HtmlWriter


def main(args):
    families = get_efloras_families(args)

    rows = reader.reader(args, families)
    rows = sorted(rows, key=lambda r: (r.flora_id, r.family, r.taxon))

    nlp = pipeline.build()
    for row in rows:
        doc = nlp(row.text)
        row.traits = [e._.data for e in doc.ents]

    if args.out_csv:
        writer = CsvWriter(args.out_csv, args.csv_min)
        writer.write(rows)

    if args.out_html:
        writer = HtmlWriter(args.out_html)
        writer.write(rows)


def get_efloras_families(args):
    families = {k: v for k, v in reader.get_families().items() if v["count"]}

    if not check_family_flora_ids(args, families):
        sys.exit(1)

    if args.list_families:
        print_families(families)
        sys.exit()

    return families


def check_family_flora_ids(args, families):
    combos = reader.get_family_flora_ids(args, families)

    flora = {i: False for i in args.flora_id}
    fams = {f: False for f in args.family}
    for combo in combos:
        fams[combo[0]] = True
        flora[combo[1]] = True

    ok = True
    for fam, hit in fams.items():
        if not hit:
            ok = False
            print(f'Family "{fam}" is not being used.')

    for id_, hit in flora.items():
        if not hit:
            ok = False
            print(f'Flora ID "{id_}" is not being used.')

    return ok


def print_families(families):
    template = "{:<20} {:>8} {:>8} {:<30}  {:<20} {:<20} {:>8}"

    print(
        template.format(
            "Family",
            "Taxon Id",
            "Flora Id",
            "Flora Name",
            "Directory Created",
            "Directory Modified",
            "Treatments",
        )
    )

    for family in families.values():
        print(
            template.format(
                family["family"],
                family["taxon_id"],
                family["flora_id"],
                family["flora_name"],
                family["created"],
                family["modified"],
                family["count"] if family["count"] else "",
            )
        )


def parse_args():
    description = """Parse data from flora website."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--family", "-f", action="append", help="""Which family to extract."""
    )

    arg_parser.add_argument(
        "--genus",
        "-g",
        action="append",
        help="""Which genus to extract with in the family. Default is
            to select all genera. Although this is designed for selecting
            genera this is really just a filter on the taxa names so you
            can put in anything that matches a taxon name.""",
    )

    flora_ids = reader.get_flora_ids()
    arg_parser.add_argument(
        "--flora-id",
        "-e",
        action="append",
        choices=[str(k) for k in flora_ids],
        help="""Which flora ID to extract. Default 1.""",
    )

    arg_parser.add_argument(
        "--out-html",
        "-H",
        type=Path,
        help="""Output the results to this HTML file.""",
    )

    arg_parser.add_argument(
        "--out-csv",
        "-C",
        type=Path,
        metavar="PATH",
        help="""Output the results to this CSV file.""",
    )

    arg_parser.add_argument(
        "--csv-min",
        type=int,
        default=3,
        metavar="MIN",
        help="""Only output to the CSV only if the trait has at least this many records.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--list-families",
        "-l",
        action="store_true",
        help="""List families available to extract and exit.""",
    )

    args = arg_parser.parse_args()

    if args.family:
        args.family = [f.lower() for f in args.family]
    else:
        args.family = []

    if args.flora_id:
        args.flora_id = [int(i) for i in args.flora_id]
    else:
        args.flora_id = [1]

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
