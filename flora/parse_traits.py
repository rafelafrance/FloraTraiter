#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib import parser
from pylib.readers.label_reader import LabelReader
from pylib.writers.label_html_writer import HtmlWriter
from traiter.pylib import log


def main():
    log.started()
    args = parse_args()

    labels = parser.parse(args)

    if args.jsonl_dir:
        ...

    if args.out_html:
        reader = LabelReader(args)
        writer = HtmlWriter(args.out_html, args.spotlight)
        writer.write(reader.labels, args)

    log.finished()


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract floral trait information from text files.

            Label images are not required but when you use them
            the text and label image file stems must match.

            A file stem is a file name without the directories and
            without the file suffix:
            /my_dir/stuff/my_label.txt -> my_label
            """
        ),
    )

    arg_parser.add_argument(
        "--text-dir",
        metavar="PATH",
        type=Path,
        required=True,
        help="""Directory containing the input text files.""",
    )

    arg_parser.add_argument(
        "--label-dir",
        metavar="PATH",
        type=Path,
        help="""Directory containing the images of labels.""",
    )

    arg_parser.add_argument(
        "--jsonl-dir",
        metavar="PATH",
        type=Path,
        help="""Output JSONL trait files to this directory.""",
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
        "--spotlight",
        metavar="TRAIT",
        help="""This trait will get its own color for HTML output.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
