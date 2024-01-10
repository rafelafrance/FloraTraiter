#!/usr/bin/env python3
import argparse
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import urlopen

import tomlkit

PYPROJECT_TOML = Path() / "pyproject.toml"


@dataclass
class Subtree:
    prefix: str
    url: str
    repo: str
    deps: set[str] = field(default_factory=set)


def main():
    _args = parse_args()
    subtrees = get_subtrees()
    get_deps(subtrees)
    deps = merge_deps(subtrees)

    with PYPROJECT_TOML.open() as f:
        pyproject = tomlkit.load(f)

    pyproject["project"]["dependencies"] = tomlkit.array()
    for dep in sorted(deps):
        pyproject["project"]["dependencies"].add_line(dep)

    with PYPROJECT_TOML.open("w") as f:
        tomlkit.dump(pyproject, f)


def merge_deps(subtrees: list[Subtree]) -> list[str]:
    deps = {"tomlkit"}
    for tree in subtrees:
        deps |= tree.deps
    return sorted(deps)


def get_deps(subtrees: list[Subtree]) -> None:
    for tree in subtrees:
        settings = urlopen(tree.url).read().decode("utf-8")  # noqa: S310
        project = tomlkit.loads(settings)
        tree.deps = set(project["project"]["dependencies"])


def get_subtrees() -> list[Subtree]:
    subtrees = []

    branch = 3  # Offset of word in checkout -b command holding the prefix
    make_file = Path() / "Makefile"

    with make_file.open() as f:
        for ln in f.readlines():
            if ln.find("remote add") > -1:
                *_, repo, url = ln.split()
                url = url.replace("github.com", "raw.githubusercontent.com")
                url = url.removesuffix(".git") + "/main/pyproject.toml"

            elif ln.find("git checkout -b") > -1:
                prefix = ln.split()[branch]
                prefix = prefix.removeprefix("upstream/")

                subtrees.append(Subtree(prefix=prefix, url=url, repo=repo))

    return subtrees


def parse_args():
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Update pyproject.toml with dependencies from subtrees.

            It finds the subtrees and downloads the pyproject.toml for each from github
            and builds a combined dependencies section from all of the subtree versions.
            """,
        ),
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
