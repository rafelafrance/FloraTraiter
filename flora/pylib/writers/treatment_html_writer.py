from dataclasses import dataclass

from tqdm import tqdm

from flora.pylib import const
from flora.pylib.treatments import Treatments
from flora.pylib.writers.base_html_writer import BaseHtmlWriter, BaseHtmlWriterRow


@dataclass(kw_only=True)
class HtmlWriterRow(BaseHtmlWriterRow):
    treatment_id: str = ""
    word_count: int = 0
    valid_words: int = 0
    score: float = 0.0


class HtmlWriter(BaseHtmlWriter):
    def __init__(self, html_file, spotlight=""):
        super().__init__(
            template_dir=f"{const.ROOT_DIR}/flora/pylib/writers/templates",
            template="treatment_html_writer.html",
            html_file=html_file,
            spotlight=spotlight,
        )

    def write(self, treatments: Treatments, args=None):
        for treat in tqdm(treatments.treatments, desc="write"):
            self.formatted.append(
                HtmlWriterRow(
                    treatment_id=treat.path.stem,
                    formatted_text=self.format_text(treat, exclude=["trs"]),
                    formatted_traits=self.format_traits(treat),
                    word_count=treat.word_count,
                    valid_words=treat.valid_words,
                    score=treat.score,
                ),
            )

        summary = {
            "Total treatments:": len(treatments.treatments),
        }

        self.write_template(args.text_dir, summary=summary)
