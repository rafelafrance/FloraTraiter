#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

import rich
from bs4 import BeautifulSoup
from pylib.text_assembler import find_lines
from pylib.text_assembler import Page
from pylib.text_assembler import page_flow
from pylib.text_assembler import Word
from traiter.pylib import log


def main():
    args = parse_args()
    log.started()

    xhtml_to_text(args)

    msg = " ".join(
        """You may want to remove headers, footers,
        figure captions (& text), map captions (& text), etc.
        from this text file.""".split()
    )
    rich.print(f"\n[bold yellow]{msg}[/bold yellow]\n")

    log.finished()


def xhtml_to_text(args):
    pages = read_xhtml(args.in_xhtml, args.min_y, args.max_y)

    with open(args.out_text, "w") as out_text:
        for page in pages:
            lines = find_lines(page)
            page.lines = lines if args.gap_min < 1 else page_flow(args, page, lines)

            for ln in page.lines:
                print(ln.text, file=out_text)

            print(file=out_text)


def read_xhtml(in_html, min_y, max_y):
    pages = []

    with open(in_html) as in_html:
        doc = in_html.read()

    soup = BeautifulSoup(doc, features="lxml")

    for no, page_elem in enumerate(soup.findAll("page"), 1):
        width = float(page_elem.attrs["width"])
        height = float(page_elem.attrs["height"])
        page = Page(no, width, height)
        pages.append(page)
        bottom = page.height - max_y

        words = []
        for word_elem in page_elem.findAll("word"):
            x_min = round(float(word_elem["xmin"]))
            y_min = round(float(word_elem["ymin"]))
            x_max = round(float(word_elem["xmax"]))
            y_max = round(float(word_elem["ymax"]))
            if y_max >= min_y and y_min <= bottom:
                words.append(Word(x_min, y_min, x_max, y_max, word_elem.text))

        page.words = sorted(words, key=lambda w: w.x_min)

    return pages


def parse_args():
    description = """Convert an XHTML file with word bounding boxes to text."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-xhtml",
        type=Path,
        required=True,
        metavar="PATH",
        help="""The XHTML file with the bounding boxes.""",
    )

    arg_parser.add_argument(
        "--out-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the text to this file.""",
    )

    arg_parser.add_argument(
        "--gap-radius",
        type=int,
        default=20,
        help="""Consider a gap to be in the center if it is within this distance of
            the true center of the page. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--gap-min",
        type=int,
        default=8,
        help="""Break a line into 2 columns if the gap between words is near the
            center and the gap is at least this big. Set this to zero if there are
            never 2 columns of text. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--min-y",
        type=int,
        default=75,
        help="""Remove words that are above this distance from the top of the page.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--max-y",
        type=int,
        default=0,
        help="""Remove words that are below this distance from the bottom of the page.
            (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
