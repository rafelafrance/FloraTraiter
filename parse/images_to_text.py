#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

import pylib.text_assembler as ta
import rich
from PIL import Image
from pylib import image_transformer as it
from pylib.ocr import tesseract_engine
from tqdm import tqdm
from traiter.pylib import log


def main():
    args = parse_args()
    log.started()

    page_images_to_text(args)

    msg = " ".join(
        """You may want to remove headers, footers, figure captions, map captions, etc.
        from this text file.""".split()
    )
    rich.print(f"\n[bold yellow]{msg}[/bold yellow]\n")

    log.finished()


def page_images_to_text(args):
    """Convert images of PDF pages into text via OCR."""
    pages = ocr_images(
        args.image_dir, args.min_y, args.max_y, args.conf, args.transform
    )
    with open(args.out_text, "w") as out_text:
        for page in pages:
            lines = ta.find_lines(page)
            page.lines = lines if args.gap_min < 1 else ta.page_flow(args, page, lines)

            for ln in page.lines:
                print(ln.text, file=out_text)

            print(file=out_text)


def ocr_images(image_dir, min_y, max_y, conf, transform):
    pages = []
    paths = sorted(image_dir.glob("*.jpg"))

    for no, path in tqdm(enumerate(paths, 1)):
        image = Image.open(path)
        if transform:
            image = it.transform_label(transform, image)

        width, height = (float(s) for s in image.size)
        page = ta.Page(no, width, height)
        pages.append(page)
        bottom = page.height - max_y

        words = []
        for frag in tesseract_engine(image):
            if (
                frag["bottom"] >= min_y
                and frag["top"] <= bottom
                and frag["conf"] >= conf
            ):
                words.append(
                    ta.Word(
                        frag["left"],
                        frag["top"],
                        frag["right"],
                        frag["bottom"],
                        frag["text"],
                    )
                )
        page.words = sorted(words, key=lambda w: w.x_min)

    return pages


def parse_args():
    """Process command-line arguments."""
    description = """Convert images of PDF pages into text via OCR."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--image-dir",
        type=Path,
        required=True,
        metavar="DIR",
        help="""The directory with the images of the pages.""",
    )

    arg_parser.add_argument(
        "--out-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the text to this file.""",
    )

    transforms = list(it.TRANSFORM_PIPELINES.keys())
    arg_parser.add_argument(
        "--transform",
        choices=transforms,
        help="""Transform images using the given pipeline in an attempt to improve OCR
            quality.""",
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

    arg_parser.add_argument(
        "--conf",
        type=float,
        default=0.0,
        help="""Only keep OCR fragments that have a confidence >= to this. Set it to
            0.0 to get everything. (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
