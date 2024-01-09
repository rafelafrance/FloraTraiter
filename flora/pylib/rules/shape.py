import re
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
class Shape(Linkable):
    # Class vars ----------
    shape_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "shape_terms.csv"
    shape_loc: ClassVar[list[str]] = ["shape_term", "shape_leader", "part_location"]
    replace: ClassVar[dict[str, str]] = term_util.term_data(shape_csv, "replace")
    # ---------------------

    shape: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.shape})

    @property
    def key(self) -> str:
        return self.key_builder("shape")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="shape_terms", path=cls.shape_csv)
        add.trait_pipe(
            nlp,
            name="shape_patterns",
            compiler=cls.shape_patterns(),
            overwrite=["count"],
        )
        add.cleanup_pipe(nlp, name="shape_cleanup")

    @classmethod
    def shape_patterns(cls):
        return [
            Compiler(
                label="shape",
                on_match="shape_match",
                keep="shape",
                decoder={
                    "-": {"TEXT": {"IN": t_const.DASH}},
                    "-/to": {"LOWER": {"IN": [*t_const.DASH, "to", "_"]}},
                    "9": {"IS_DIGIT": True},
                    "angular": {"LOWER": {"IN": ["angular", "angulate"]}},
                    "shape": {"ENT_TYPE": "shape_term"},
                    "shape_leader": {"ENT_TYPE": "shape_leader"},
                    "shape_loc": {"ENT_TYPE": {"IN": cls.shape_loc}},
                    "shape_word": {"ENT_TYPE": {"IN": ["shape_term", "shape_leader"]}},
                },
                patterns=[
                    "shape_loc*   -*    shape+",
                    "shape_loc*   -*    shape       -* shape+",
                    "shape_leader -/to+ shape_word+ -* shape+",
                    "shape_word+  -*    shape+",
                    "shape_loc* 9 -     angular",
                ],
            ),
        ]

    @classmethod
    def shape_match(cls, ent):
        # Handle 3-angular etc.
        if re.match(r"^\d", ent.text):
            shape = "polygonal"

        # All other shapes
        else:
            shape = {}  # Dicts preserve order sets do not
            for token in ent:
                if token._.term == "shape_term" and token.text != "-":
                    word = cls.replace.get(token.lower_, token.lower_)
                    shape[word] = 1
            shape = "-".join(shape)
            shape = cls.replace.get(shape, shape)

        return cls.from_ent(ent, shape=shape)


@registry.misc("shape_match")
def shape_match(ent):
    return Shape.shape_match(ent)
