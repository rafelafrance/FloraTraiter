from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from .linkable import Linkable


@dataclass(eq=False)
class Margin(Linkable):
    # Class vars ----------
    margin_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "margin_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data(margin_csv, "replace")
    # ---------------------

    margin: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.margin})

    @property
    def key(self) -> str:
        return self.key_builder("margin")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="margin_terms", path=cls.margin_csv)
        add.trait_pipe(nlp, name="margin_patterns", compiler=cls.margin_patterns())
        add.cleanup_pipe(nlp, name="margin_cleanup")

    @classmethod
    def margin_patterns(cls):
        return [
            Compiler(
                label="margin",
                on_match="margin_match",
                keep="margin",
                decoder={
                    "-": {"TEXT": {"IN": t_const.DASH}},
                    "margin": {"ENT_TYPE": "margin_term"},
                    "shape": {"ENT_TYPE": "shape"},
                    "leader": {"ENT_TYPE": {"IN": ["shape", "margin_leader"]}},
                    "follower": {
                        "ENT_TYPE": {"IN": ["margin_term", "margin_follower"]},
                    },
                },
                patterns=[
                    "leader* -* margin+",
                    "leader* -* margin -* follower*",
                    "leader* -* margin -* shape? follower+ shape?",
                    "shape+ -* follower+",
                ],
            ),
        ]

    @classmethod
    def margin_match(cls, ent):
        margin = {}  # Dicts preserve order sets do not
        for token in ent:
            if token._.term in ["margin_term", "shape"] and token.text != "-":
                word = cls.replace.get(token.lower_, token.lower_)
                margin[word] = 1
        margin = "-".join(margin.keys())
        margin = cls.replace.get(margin, margin)
        return cls.from_ent(ent, margin=margin)


@registry.misc("margin_match")
def margin_match(ent):
    return Margin.margin_match(ent)
