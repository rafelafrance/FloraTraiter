#!/usr/bin/env python3
import argparse
import json
import textwrap
from pathlib import Path

from traiter.pylib.darwin_core import DarwinCore
from util.pylib import log

from old.traits import Traits


def main():
    log.started()
    args = parse_args()

    all_traits: list[Traits] = [Traits(p) for p in sorted(args.text_dir.glob("*"))]
    all_traits.parse()

    args.traiter_dir.mkdir(parents=True, exist_ok=True)
    write_json(all_traits, args.json_dir)

    log.finished()


def get_text(text_dir, limit=None):
    all_traits = [Traits(p) for p in sorted(text_dir.glob("*"))]
    return all_traits[0:limit] if limit else all_traits


def write_json(treatments: list[Traits], json_dir):
    for treat in treatments.treatments:
        dwc = DarwinCore()
        _ = [t.to_dwc(dwc) for t in treat.traits]

        path = json_dir / f"{treat.path.stem}.json"
        with path.open("w") as f:
            traits = dwc.to_dict()
            traits["treatment"] = treat.text
            json.dump(traits, f, indent=4)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract trait information from text files containing treatments, labels,
            or whatever. Each input file contains a single item to parse.
            """,
        ),
    )

    arg_parser.add_argument(
        "--text-dir",
        metavar="PATH",
        type=Path,
        required=True,
        help="""Directory containing the input text files. Each file is a single
            treatment, label, etc.""",
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
        help="""Read this many treatments for input. Useful for testing.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
