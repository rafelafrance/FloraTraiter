from dataclasses import dataclass

from tqdm import tqdm

from flora.pylib import const

from .base_html_writer import BaseHtmlWriter, BaseHtmlWriterRow


# @dataclass(kw_only=True)
@dataclass
class HtmlWriterRow(BaseHtmlWriterRow):
    family: str = ""
    flora_id: int = ""
    taxon: str = ""
    taxon_id: int = -1
    link: str = ""
    path: str = ""


class HtmlWriter(BaseHtmlWriter):
    def __init__(self, html_file):
        super().__init__(
            template_dir=f"{const.ROOT_DIR}/pylib/writers/templates",
            template="efloras_html_writer.html",
            html_file=html_file,
        )

    def write(self, efloras_rows, in_file_name=""):
        for efloras_row in tqdm(efloras_rows):
            text = self.format_text(efloras_row)
            traits = self.format_traits(efloras_row)
            self.formatted.append(
                HtmlWriterRow(
                    formatted_text=text,
                    formatted_traits=traits,
                    family=efloras_row.family,
                    flora_id=efloras_row.flora_id,
                    taxon=efloras_row.taxon,
                    taxon_id=efloras_row.taxon_id,
                    link=efloras_row.link,
                    path=efloras_row.path,
                ),
            )

        self.write_template(in_file_name)
