from dataclasses import dataclass

from tqdm import tqdm

from flora.pylib import const
from flora.pylib.writers.base_html_writer import BaseHtmlWriter
from flora.pylib.writers.base_html_writer import BaseHtmlWriterRow


@dataclass(kw_only=True)
class HtmlWriterRow(BaseHtmlWriterRow):
    label_id: str = ""
    label_image: str = ""
    word_count: int = 0
    valid_words: int = 0
    score: float = 0.0


class HtmlWriter(BaseHtmlWriter):
    def __init__(self, out_html, spotlight=""):
        super().__init__(
            template_dir=f"{const.ROOT_DIR}/flora/pylib/writers/templates",
            template="label_html_writer.html",
            out_html=out_html,
            spotlight=spotlight,
        )

    def write(self, labels, args=None):
        length_cutoff, score_cutoff = 0, 0

        for lb in tqdm(labels.labels, desc="write"):
            if lb.word_count < args.length_cutoff:
                length_cutoff += 1
                continue

            if lb.score < args.score_cutoff:
                score_cutoff += 1
                continue

            self.formatted.append(
                HtmlWriterRow(
                    label_id=lb.path.stem,
                    formatted_text=self.format_text(lb, exclude=["trs"]),
                    formatted_traits=self.format_traits(lb),
                    label_image=lb.encoded_image,
                    word_count=lb.word_count,
                    valid_words=lb.valid_words,
                    score=lb.score,
                )
            )

        total = len(labels.labels)
        summary = [
            (
                f"Total labels = {total}"
                f"kept = {total - length_cutoff - score_cutoff}"
            ),
            f"total removed = {length_cutoff + score_cutoff}",
            f"too short = {length_cutoff} (threshold {args.length_cutoff})",
            f"score too low = {score_cutoff} (threshold {args.score_cutoff})",
        ]

        self.write_template(args.text_dir, summary=summary)
