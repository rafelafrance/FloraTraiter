#!/usr/bin/env python3
import argparse
import logging
import textwrap
from pathlib import Path

import ftfy
import regex as re
import rich
from traiter.pylib import log
from traiter.pylib.pipes import sentence

MOJIBAKE = {
    "{": "(",
    "}": ")",
}

MOJIBAKE_WORDS = {
    # "find": "replace"
    r"Ivd": "lvd",
    r"Ivs": "lvs",
    r"1vd": "lvd",
    r"If-": "lf-",
    r"1f-": "lf-",
    r"If\.": "lf.",
    r"1f\.": "lf.",
    r"(?<=[a-z])U": "ll",
    r"-\s?l\b": "-1",
    r"\bl\s?-": "1-",
    r"-\s?l\s?l\b": "-11",
    r"\bl\s?l\s?-": "11-",
    r"\bl\s?1\b": "11",
    r"\bm\sm\b": "mm",
    r"1obe": "lobe",
    r"1eave": "leave",
    r"1eaf": "leaf",
    r"[Ili]\.(?=\d)": "1.",
    r"Unear": "Linear",
    r"tmnk": "trunk",
    r"(?<=[A-Za-z])/(?=[A-Za-z])": "l",
    r"//": "H",
    r"yar\.": "var.",
    r"var,": "var.",
    r"subsp,": "subsp.",
}

MOJIBAKE_REPLACE = {}


def main():
    args = parse_args()
    log.started()

    clean(args)

    msg = "You may want to look over and edit the output text."
    rich.print(f"\n[bold yellow]{msg}[/bold yellow]\n")

    log.finished()


def clean(args):
    with open(args.in_text) as raw_file:
        text = raw_file.read()

    # The bulk of the text cleaning happens in this function
    logging.info("Cleaning text")
    trans = str.maketrans(MOJIBAKE)
    regexp = build_replace_patterns()
    text = clean_text(text, trans=trans, regexp=regexp)

    # Break into sentences
    logging.info("Breaking text into sentences")
    nlp = sentence.pipeline()
    nlp.max_length = args.nlp_max_length
    doc = nlp(text)

    # Write output
    lines = [s.text + "\n" for s in doc.sents if s and s.text]
    with open(args.out_text, "w") as clean_file:
        clean_file.writelines(lines)


def clean_text(
    text: str,
    trans: dict[int, str] = None,
    regexp: re.regex = None,
) -> str:
    text = text if text else ""

    text = text.translate(trans)  # Handle uncommon mojibake

    text = replace_patterns(regexp, text)  # Replace messed up words

    text = " ".join(text.split())  # Space normalize

    # Join hyphenated words when they are at the end of a line
    text = re.sub(r"([a-z])-\s+([a-z])", r"\1\2", text, flags=re.IGNORECASE)

    text = re.sub(r"(\d) (\d)", r"\1\2", text)  # Handle spaces between digits

    text = ftfy.fix_text(text)  # Handle common mojibake

    text = re.sub(r"\p{Cc}+", " ", text)  # Remove control characters

    return text


def build_replace_patterns() -> re.regex:
    replaces = []
    for i, (pattern, repl) in enumerate(MOJIBAKE_WORDS.items()):
        re_group_name = f"X{i:04d}"
        MOJIBAKE_REPLACE[re_group_name] = repl
        replaces.append(f"(?P<{re_group_name}>{pattern})")
    regexp: re.regex = re.compile("|".join(replaces))
    return regexp


def replace_patterns(regexp: re.regex, text: str) -> str:
    text = regexp.sub(lambda m: MOJIBAKE_REPLACE[m.lastgroup], text)
    return text


def parse_args():
    description = """Clean text to prepare it for trait extraction."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Which text file to clean.""",
    )

    arg_parser.add_argument(
        "--out-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the cleaned text to this file.""",
    )

    arg_parser.add_argument(
        "--nlp-max-length",
        type=int,
        default=5,
        metavar="MB",
        help="""The maximum text file size to process. This is given in megabytes.
            This is a spaCy constraint. (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    args.nlp_max_length *= 1_000_000
    return args


if __name__ == "__main__":
    main()
