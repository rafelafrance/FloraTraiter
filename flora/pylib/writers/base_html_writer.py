import html
import itertools
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, NamedTuple

import jinja2
from traiter.pylib.darwin_core import DYN, DarwinCore

from flora.pylib.label import Label
from flora.pylib.labels import Labels

COLOR_COUNT = 14
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])


class TraitRow(NamedTuple):
    label: str
    data: Any


class Sortable(NamedTuple):
    key: str
    start: int
    dwc: str
    title: str


@dataclass(kw_only=True)
class BaseHtmlWriterRow:
    formatted_text: str
    formatted_traits: list[TraitRow] = field(default_factory=list)


class CssClasses:
    def __init__(self, spotlight: str = ""):
        self.classes = {}
        self.spotlight = spotlight

    def __getitem__(self, key):
        if self.spotlight and key.find(self.spotlight) > -1:
            return "ccx"
        if key not in self.classes:
            self.classes[key] = next(BACKGROUNDS)
        return self.classes[key]


class BaseHtmlWriter:
    def __init__(self, template_dir, template, html_file, spotlight=""):
        self.template_dir = template_dir
        self.template = template
        self.html_file = html_file
        self.css_classes = CssClasses(spotlight)
        self.formatted = []

    def write(self, rows: Labels, args=None):
        raise NotImplementedError

    def format_text(self, row: Label, exclude=None):
        """Wrap traits in the text with <spans> that can be formatted with CSS."""
        exclude = exclude if exclude else []
        frags = []
        prev = 0

        for trait in row.traits:
            if trait.trait in exclude:
                continue

            start = trait.start
            end = trait.end

            if prev < start:
                frags.append(html.escape(row.text[prev:start]))

            cls = self.css_classes[trait.key]

            dwc = DarwinCore()
            dwc = trait.to_dwc(dwc).to_dict()

            title = ", ".join(f"{k}:&nbsp;{v}" for k, v in dwc.items())

            frags.append(f'<span class="{cls}" title="{title}">')
            frags.append(html.escape(row.text[start:end]))
            frags.append("</span>")
            prev = end

        if len(row.text) > prev:
            frags.append(html.escape(row.text[prev:]))

        text = "".join(frags)
        return text

    def format_traits(self, row):
        """Group traits for display in their own table."""
        traits = []

        sortable = []
        for trait in row.traits:
            dwc = DarwinCore()
            sortable.append(
                Sortable(
                    trait.key,
                    trait.start,
                    trait.to_dwc(dwc),
                    row.text[trait.start : trait.end],
                ),
            )

        sortable = sorted(sortable)

        for key, grouped in itertools.groupby(sortable, key=lambda x: x.key):
            cls = self.css_classes[key]
            label = f'<span class="{cls}">{key}</span>'
            trait_list = []
            for trait in grouped:
                fields = {}
                dwc_dict = trait.dwc.to_dict()
                for k, v in dwc_dict.items():
                    fields = v if k == DYN else dwc_dict
                fields = ", ".join(
                    f'<span title="{trait.title}">{k}:&nbsp;{v}</span>'
                    for k, v in fields.items()
                )
                if fields:
                    trait_list.append(fields)

            if trait_list:
                traits.append(
                    TraitRow(label, '<br/><hr class="sep"/>'.join(trait_list)),
                )

        return traits

    def write_template(self, in_file_name="", image_dir="", summary=None):
        summary = summary if summary else {}
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True,
        )

        template = env.get_template(self.template).render(
            now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
            file_name=in_file_name,
            image_dir=image_dir,
            rows=self.formatted,
            summary=summary,
        )

        with self.html_file.open("w") as html_file:
            html_file.write(template)
