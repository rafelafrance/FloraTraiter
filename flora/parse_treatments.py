#!/usr/bin/env python3
import argparse
import json
import textwrap
from pathlib import Path

from pylib.treatments import Treatments
from pylib.writers.treatment_html_writer import HtmlWriter
from traiter.pylib.darwin_core import DarwinCore
from util.pylib import log


def main():
    log.started()
    args = parse_args()

    treatments: Treatments = Treatments(args)
    treatments.parse()

    if args.html_file:
        writer = HtmlWriter(args.html_file, args.spotlight)
        writer.write(treatments, args.traiter_dir)

    if args.csv_file:
        ...

    if args.traiter_dir:
        args.traiter_dir.mkdir(parent=True, exist_ok=True)
        write_json(treatments, args.traiter_dir)

    log.finished()


def write_json(treatments: Treatments, traiter_dir):
    for treat in treatments.treatments:
        dwc = DarwinCore()
        _ = [t.to_dwc(dwc) for t in treat.traits]

        path = traiter_dir / f"{treat.path.stem}.json"
        with path.open("w") as f:
            json.dump(dwc.to_dict(), f, indent=4)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract floral trait information from text files containing treatments.
            Each input file contains a single treatment.
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
        "--traiter-dir",
        metavar="PATH",
        type=Path,
        help="""Output JSON files holding traits, one for each input text file, in this
            directory.""",
    )

    arg_parser.add_argument(
        "--csv-file",
        type=Path,
        metavar="PATH",
        help="""Output CSV formatted results to this file.""",
    )

    arg_parser.add_argument(
        "--html-file",
        type=Path,
        metavar="PATH",
        help="""Output HTML formatted results to this file.""",
    )

    arg_parser.add_argument(
        "--limit",
        type=int,
        help="""Read this many treatments for input.""",
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
