#!/usr/bin/env python3
import argparse
import shutil
import textwrap
from pathlib import Path

import rich


def main():
    args = parse_args()

    paths = sorted(args.dir.glob(args.glob))
    for src in paths:
        parts = src.stem.split("_")
        if len(parts) != 2:
            continue
        try:
            _ = int(parts[1])
            stem = f"{parts[0]}_{parts[1].zfill(3)}"
            dst = src.with_stem(stem)
            shutil.move(src, dst)
        except ValueError:
            rich.print(f"Could not rename: [bold red]{src}[/bold red]")
            continue


def parse_args():
    """Process command-line arguments."""
    description = """Fix image numbers."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--dir",
        type=Path,
        required=True,
        metavar="DIR",
        help="""The directory with messed up numbering.""",
    )

    arg_parser.add_argument(
        "--glob",
        default="*.jpg",
        help="""What files to change. (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
