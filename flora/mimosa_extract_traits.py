#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib.readers.mimosa_marked_reader import MarkedReader
from pylib.readers.mimosa_proximity_reader import ProximityReader
from pylib.writers.mimosa_csv_writer import CsvWriter
from pylib.writers.mimosa_html_writer import HtmlWriter
from traiter.pylib import log


def main():
    args = parse_args()
    log.started()

    reader = ProximityReader(args) if args.reader == "proximity" else MarkedReader(args)
    traits_in_text, traits_by_taxon = reader.read()

    if args.csv_file:
        writer = CsvWriter(args.csv_file, args.csv_min)
        writer.write(traits_by_taxon)

    if args.html_file:
        writer = HtmlWriter(args.html_file)
        writer.write(traits_in_text, args.in_text.stem)

    log.finished()


def parse_args():
    description = """Parse data about mimosas from PDFs converted into text files."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars="@",
    )

    arg_parser.add_argument(
        "--in-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Which text file (a converted PDF) to process.""",
    )

    arg_parser.add_argument(
        "--reader",
        choices=["proximity", "marked"],
        default="marked",
        help="""Which reader to use. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--html-file",
        type=Path,
        metavar="PATH",
        help="""Output the results to this HTML file.""",
    )

    arg_parser.add_argument(
        "--csv-file",
        type=Path,
        metavar="PATH",
        help="""Output the results to this CSV file.""",
    )

    arg_parser.add_argument(
        "--pattern",
        default="A taxon starts here.",
        help="""This pattern demarcates where a treatment for a particular taxon starts.
            You will often have to quote this argument. (default: %(default)s)""",
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
        "--taxon-distance",
        type=int,
        default=2,
        metavar="INT",
        help="""How long before we need too see a taxon name. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--limit",
        type=int,
        metavar="LIMIT",
        help="""Limit the input to this many records.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
