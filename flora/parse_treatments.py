#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from util.pylib import log

from flora.pylib import const
from flora.pylib.treatments import Treatments
from flora.pylib.writers.csv_writer import write_csv
from flora.pylib.writers.html_writer import HtmlWriter
from flora.pylib.writers.json_writer import write_json


def main():
    log.started()
    args = parse_args()

    treatments: Treatments = Treatments(args.treatment_dir, args.limit, args.offset)
    treatments.parse(encoding=args.encoding)

    if args.html_file:
        writer = HtmlWriter(
            template_dir=f"{const.ROOT_DIR}/flora/pylib/writers/templates",
            template="treatment_html_writer.html",
            html_file=args.html_file,
            spotlight=args.spotlight,
        )
        writer.write(treatments, args)

    if args.csv_file:
        write_csv(treatments, args.csv_file)

    if args.json_dir:
        write_json(treatments, args.json_dir)

    log.finished()


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract floral trait information from treatment text extracted
            from PDFs or web pages.
            """,
        ),
    )

    arg_parser.add_argument(
        "--treatment-dir",
        metavar="PATH",
        type=Path,
        required=True,
        help="""Directory containing the input treatment text files.""",
    )

    arg_parser.add_argument(
        "--html-file",
        type=Path,
        metavar="PATH",
        help="""Output HTML formatted results to this file.""",
    )

    arg_parser.add_argument(
        "--csv-file",
        type=Path,
        metavar="PATH",
        help="""Output results to this CSV file.""",
    )

    arg_parser.add_argument(
        "--json-dir",
        metavar="PATH",
        type=Path,
        help="""Output JSON files holding traits, one for each input text file, in this
            directory.""",
    )

    arg_parser.add_argument(
        "--limit",
        type=int,
        help="""Read this many treatments for input.""",
    )

    arg_parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="""Offset for splitting data.""",
    )

    arg_parser.add_argument(
        "--spotlight",
        metavar="TRAIT",
        help="""This trait will get its own color for HTML output.""",
    )

    arg_parser.add_argument(
        "--encoding",
        metavar="ENCODING",
        default="utf8",
        help="""What encoding is used for the input file. These should be Western
        European encodings; that's what the parsers are designed for.
        (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
