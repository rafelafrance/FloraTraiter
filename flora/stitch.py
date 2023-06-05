#!/usr/bin/env python3
import argparse
import json
import textwrap
from dataclasses import dataclass
from pathlib import Path

import pylib.text_assembler as ta
from PIL import Image
from pylib import image_transformer as it
from pylib.ocr import tesseract_engine
from tqdm import tqdm
from traiter.pylib import log


@dataclass
class Box:
    x0: int = None
    y0: int = None
    x1: int = None
    y1: int = None
    start: bool = False


def main():
    args = parse_args()
    log.started()

    with open(args.in_json) as in_json:
        page_data = json.load(in_json)

    with open(args.out_text, "w") as out_text:
        for json_page in tqdm(page_data):
            if not json_page["boxes"]:
                continue

            image = Image.open(json_page["path"])
            if args.transform:
                image = it.transform_label(args.transform, image)

            for box in json_page["boxes"]:
                box = Box(**box)

                resize(json_page, image, box)  # ################################
                cropped = image.crop((box.x0, box.y0, box.x1, box.y1))

                page = ta.Page()

                words = []
                for frag in tesseract_engine(cropped):
                    if frag["conf"] >= args.conf:
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
                page.lines = ta.find_lines(page)

                if box.start:
                    print(args.pattern, file=out_text)

                for ln in page.lines:
                    print(ln.text, file=out_text)

    log.finished()


# #############################################
def resize(page, image, box):
    image_width, image_height = image.size
    ratio = image_height / page["photo_y"]
    box.x0 = int(ratio * box.x0)
    box.y0 = int(ratio * box.y0)
    box.x1 = int(ratio * box.x1)
    box.y1 = int(ratio * box.y1)


def parse_args():
    description = """Clean text to prepare it for trait extraction."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--in-json",
        type=Path,
        required=True,
        metavar="PATH",
        help="""JSON file that holds the output of the stitch.py script.""",
    )

    arg_parser.add_argument(
        "--out-text",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output the stitched text to this file.""",
    )

    arg_parser.add_argument(
        "--pattern",
        default="A taxon starts here.",
        help="""This pattern demarcates where a treatment for a particular taxon starts
            this may be a regular expression. You will often have to quote this
            argument. (default: %(default)s)""",
    )

    transforms = list(it.TRANSFORM_PIPELINES.keys())
    arg_parser.add_argument(
        "--transform",
        choices=transforms,
        help="""Transform images using the given pipeline in an attempt to improve OCR
            quality.""",
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
