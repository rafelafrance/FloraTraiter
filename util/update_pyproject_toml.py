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

    with PYPROJECT_TOML.open() as f:
        doc = tomlkit.load(f)

    get_deps(subtrees)
    deps = merge_deps(doc, subtrees)

    update_dependencies(doc, deps)
    update_ruff(doc)

    with PYPROJECT_TOML.open("w") as f:
        tomlkit.dump(doc, f)


def update_ruff(doc):
    url = (
        "https://raw.githubusercontent.com/rafelafrance/common_utils/main/"
        "pyproject.toml"
    )
    settings = urlopen(url).read().decode("utf-8")  # noqa: S310
    project = tomlkit.loads(settings)
    doc["tool"]["ruff"] = project["tool"]["ruff"]


def update_dependencies(doc, deps):
    doc["project"]["dependencies"] = tomlkit.array()
    for dep in sorted(deps):
        doc["project"]["dependencies"].add_line(dep)
    doc["project"]["dependencies"].add_line(indent="")


def merge_deps(doc, subtrees: list[Subtree]) -> list[str]:
    deps = {"tomlkit"}
    if (
        doc.get("tool")
        and doc["tool"].get("common_utils")
        and doc["tool"]["common_utils"].get("base-dependencies")
    ):
        deps = set(doc["tool"]["common_utils"]["base-dependencies"])

    for tree in subtrees:
        deps |= tree.deps

    return sorted(deps)


def get_deps(subtrees: list[Subtree]) -> None:
    for tree in subtrees:
        print(tree.url)
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
                if ln.strip().endswith("master"):
                    url = url.replace("/main/", "/master/")

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
