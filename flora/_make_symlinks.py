#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path
from typing import NamedTuple

ROOT = Path()
MAKE_FILE = ROOT / "Makefile"
SRC = ROOT / "digi_leap"

SUB = 4  # Index of the subtree dir in the "git subtree pull" command


class Script(NamedTuple):
    tree: str
    dst: Path


def main():
    args = parse_args()
    clean_script_symlinks(args.clean_links)
    sub_trees = get_subtrees()
    scripts = get_scripts(sub_trees)
    make_script_symlinks(scripts, args.script_links)
    make_test_symlinks(sub_trees, args.test_links)


def make_script_symlinks(scripts, script_links) -> None:
    if script_links:
        for script in scripts:
            src = SRC / script.dst.name
            dst = Path("..") / script.tree / script.tree / script.dst.name
            src.symlink_to(dst)


def make_test_symlinks(sub_trees, test_links) -> None:
    if test_links:
        for tree in sub_trees:
            src = ROOT / tree / "pylib"
            dst = Path(tree) / "pylib"
            src.unlink(missing_ok=True)
            src.symlink_to(dst)


def get_subtrees() -> list[str]:
    with MAKE_FILE.open() as f:
        return [ln.split()[SUB] for ln in f.readlines() if ln.find("subtree pull") > -1]


def get_scripts(sub_trees) -> list[Script]:
    scripts = []
    for tree in sub_trees:
        path = ROOT / tree / tree
        paths = [p for p in path.glob("*.py") if not p.stem.startswith("__")]
        scripts = [Script(tree, p) for p in paths]
    return scripts


def clean_script_symlinks(clean_links) -> None:
    if clean_links:
        for link in [lnk for lnk in SRC.glob("*.py") if lnk.is_symlink()]:
            link.unlink()


def parse_args():
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Create symlinks for all scripts in subtrees.
            Scripts starting with "__" will be skipped.
            Also create symlinks need for running tests in subtrees.
            """,
        ),
    )

    arg_parser.add_argument(
        "--clean-links",
        action="store_true",
        help="""Remove old script symlinks before creating new ones.""",
    )

    arg_parser.add_argument(
        "--script-links",
        action="store_true",
        help="""Create new script symlinks.""",
    )

    arg_parser.add_argument(
        "--test-links",
        action="store_true",
        help="""Create symlinks needed for tests.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
