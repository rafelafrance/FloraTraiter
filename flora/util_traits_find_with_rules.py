#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib import validate_args
from pylib.traits import ner
from pylib.traits.label_reader import LabelReader
from pylib.traits.writers.html_writer import HtmlWriter
from traiter.pylib import log


def main():
    log.started()
    args = parse_args()

    ner.ner(args)

    if args.out_html:
        reader = LabelReader(args)
        writer = HtmlWriter(args.out_html, args.spotlight)
        writer.write(reader.labels, args)

    log.finished()


def parse_args() -> argparse.Namespace:
    description = """Extract information from the labels."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--database",
        metavar="PATH",
        type=Path,
        required=True,
        help="""Path to a digi-leap database.""",
    )

    arg_parser.add_argument(
        "--trait-set",
        required=True,
        metavar="NAME",
        help="""Name the trait set.""",
    )

    arg_parser.add_argument(
        "--ocr-set",
        required=True,
        metavar="NAME",
        help="""Extract traits from this OCR set.""",
    )

    arg_parser.add_argument(
        "--out-html",
        type=Path,
        metavar="PATH",
        help="""Output the results to this HTML file.""",
    )

    arg_parser.add_argument(
        "--score-cutoff",
        type=float,
        default=0.7,
        metavar="FRACTION",
        help="""Only keep labels if their score is this or more.
            The score is between 0.0 and 1.0. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--length-cutoff",
        type=int,
        default=10,
        metavar="LENGTH",
        help="""Only keep labels if they have at least this many words.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--limit",
        type=int,
        help="""Sample this many labels.""",
    )

    arg_parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="""Offset for splitting data.""",
    )

    arg_parser.add_argument(
        "--label-id",
        type=int,
        metavar="ID",
        help="""Select only this label ID. Used for testing.""",
    )

    arg_parser.add_argument(
        "--spotlight",
        metavar="TRAIT",
        help="""This trait will get its own color for HTML output.""",
    )

    arg_parser.add_argument(
        "--notes",
        default="",
        metavar="TEXT",
        help="""Notes about this run. Enclose them in quotes.""",
    )

    args = arg_parser.parse_args()
    validate_args.validate_ocr_set(args.database, args.ocr_set)
    return args


if __name__ == "__main__":
    main()
