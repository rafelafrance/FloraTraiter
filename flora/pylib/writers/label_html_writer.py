import base64
import io
import logging
import warnings
from dataclasses import dataclass
from pathlib import Path

import regex as re
from PIL import Image
from tqdm import tqdm
from traiter.pylib import term_util
from traiter.pylib.spell_well import SpellWell

from flora.pylib import const
from flora.pylib.traits import terms as p_terms
from flora.pylib.writers.base_html_writer import BaseHtmlWriter
from flora.pylib.writers.base_html_writer import BaseHtmlWriterRow

MAX_SIZE = 600.0  # pixels


@dataclass(kw_only=True)
class HtmlWriterRow(BaseHtmlWriterRow):
    label_id: int = 0
    label_image: str = ""
    word_count: int = 0
    spell_count: int = 0
    ratio: float = 0.0


class HtmlWriter(BaseHtmlWriter):
    def __init__(self, out_html, spotlight=""):
        super().__init__(
            template_dir=f"{const.ROOT_DIR}/digi_leap/pylib/traits/writers/templates",
            template="html_writer.html",
            out_html=out_html,
            spotlight=spotlight,
        )

        self.spell_well = SpellWell()

        self.words = {w.lower() for w in self.spell_well.vocab_to_set()}

        path = Path(p_terms.__file__).parent / "binomial_terms.zip"
        for term in term_util.read_terms(path):
            self.words |= set(term["pattern"].lower().split())

        path = Path(p_terms.__file__).parent / "monomial_terms.zip"
        self.words |= {t["pattern"] for t in term_util.read_terms(path)}

    def write(self, labels, args=None):
        length_cutoff, score_cutoff = 0, 0

        for lb in tqdm(sorted(labels, key=lambda label: label.label_id), desc="write"):
            word_count, spell_count, ratio = self.get_counts(lb)

            if word_count < args.length_cutoff:
                length_cutoff += 1
                continue

            if ratio < args.score_cutoff:
                score_cutoff += 1
                continue

            self.formatted.append(
                HtmlWriterRow(
                    label_id=lb.label_id,
                    formatted_text=self.format_text(lb, exclude=["trs"]),
                    formatted_traits=self.format_traits(lb),
                    label_image=self.get_label_image(lb),
                    word_count=word_count,
                    spell_count=spell_count,
                    ratio=ratio,
                )
            )

        total = len(labels)
        logging.info(
            f"Total labels = {total}; kept = {total - length_cutoff - score_cutoff}; "
            f"total removed = {length_cutoff + score_cutoff}; "
            f"too short: (threshold {args.length_cutoff} = {length_cutoff}; "
            f"score too low: (threshold {args.score_cutoff}) = {score_cutoff}"
        )

        self.write_template(args.trait_set)

    def get_counts(self, label):
        tokens = [t for t in re.split(r"[^\p{L}]+", label.text.lower()) if t]
        total = len(tokens)

        count = sum(1 for w in tokens if w in self.words)

        ratio = 0.0 if total == 0 else round(count / total, 2)
        return total, count, ratio

    @staticmethod
    def get_label_image(label) -> str:
        label = label.data
        with warnings.catch_warnings():  # Turn off EXIF warnings
            warnings.filterwarnings("ignore", category=UserWarning)
            path = const.ROOT_DIR / label["path"]
            sheet = Image.open(path)

        image = sheet.crop(
            (
                label["label_left"],
                label["label_top"],
                label["label_right"],
                label["label_bottom"],
            )
        )

        if image.size[1] > image.size[0]:
            width = round(MAX_SIZE / image.size[1] * image.size[0])
            image = image.resize((width, int(MAX_SIZE)))
        else:
            height = round(MAX_SIZE / image.size[0] * image.size[1])
            image = image.resize((int(MAX_SIZE), height))

        memory = io.BytesIO()
        image.save(memory, format="JPEG")
        image_bytes = memory.getvalue()

        string = base64.b64encode(image_bytes).decode()
        return string
