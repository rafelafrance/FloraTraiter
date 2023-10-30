#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from pylib.writers.label_html_writer import HtmlWriter
from traiter.pylib import log

from flora.pylib.labels import Labels


def main():
    log.started()
    args = parse_args()

    labels = Labels(args)
    labels.parse()

    if args.out_html:
        writer = HtmlWriter(args.out_html, args.spotlight)
        writer.write(labels, args)

    log.finished()


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract floral trait information from label text extracted
            from herbarium sheets.

            Images of the input label are not required but when you
            use them the text and label image file stems must match.

            A file stem is a file name without the directories and
            without the file suffix. For example:
                /my_dir/sub_dir/my_label_file.txt -> my_label_file
            """,
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
        "--text-glob",
        metavar="GLOB",
        default="*",
        help="""Only include label text files that match this pattern.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--image-dir",
        metavar="PATH",
        type=Path,
        help="""Directory containing the images of labels or treatments.
            These images are for HTML output.""",
    )

    arg_parser.add_argument(
        "--image-glob",
        metavar="GLOB",
        default="*",
        help="""Only include images that match this pattern. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--json-dir",
        metavar="PATH",
        type=Path,
        help="""Output JSON files holding traits, one for each input text file, in this
            directory.""",
    )

    arg_parser.add_argument(
        "--out-html",
        type=Path,
        metavar="PATH",
        help="""Output HTML formatted results to this file.""",
    )

    arg_parser.add_argument(
        "--darwin-core",
        "--dwc",
        action="store_true",
        help="""Use Darwin Core formatted output.""",
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
