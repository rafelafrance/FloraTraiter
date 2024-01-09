from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes.reject_match import REJECT_MATCH
from traiter.pylib.rules import terms as t_terms

from .linkable import Linkable


@dataclass(eq=False)
class Part(Linkable):
    # Class vars ----------
    part_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "part_terms.csv"
    all_csvs: ClassVar[list[Path]] = [
        part_csv,
        Path(t_terms.__file__).parent / "missing_terms.csv",
    ]

    replace: ClassVar[dict[str, str]] = term_util.term_data(all_csvs, "replace")
    type_: ClassVar[dict[str, str]] = term_util.term_data(part_csv, "type")
    # ---------------------

    # part in base class
    type: str = None
    missing: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.part})

    @property
    def key(self) -> str:
        prepend = "missing" if self.missing else None
        return self.key_builder(*self.type.split("_"), prepend=prepend, add_data=False)

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="part_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="part_patterns",
            compiler=cls.part_patterns(),
            overwrite=""" part_term part_and part_leader missing """.split(),
        )
        add.cleanup_pipe(nlp, name="part_cleanup")

    @classmethod
    def part_patterns(cls):
        decoder = {
            "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
            "and": {"ENT_TYPE": "part_and"},
            "bad_part": {"ENT_TYPE": "bad_part"},
            "leader": {"ENT_TYPE": "part_leader"},
            "missing": {"ENT_TYPE": "missing"},
            "part": {"ENT_TYPE": "part_term"},
        }

        return [
            Compiler(
                label="part",
                id="part",
                on_match="part_match",
                keep="part",
                decoder=decoder,
                patterns=[
                    "missing? leader? part+ -   part+",
                    "missing? leader? part+ and part+",
                    "missing? leader? part+",
                    "missing? leader? part+",
                ],
            ),
            Compiler(
                label="not_a_part",
                on_match=REJECT_MATCH,
                decoder=decoder,
                patterns=[
                    "- part+",
                    "- part -",
                    "bad_part",
                ],
            ),
        ]

    @classmethod
    def append_frag(cls, token, frags):
        part = cls.replace.get(token.lower_, token.lower_)
        if part not in frags[-1]:
            frags[-1].append(part)

    @classmethod
    def part_match(cls, ent):
        types = []
        frags = [[]]
        missing = None

        for sub_ent in [e for e in ent.ents if e.label_ == "part_term"]:
            text = [t.lower_ for t in sub_ent if t._.term == "part_term"]
            text = " ".join(text).replace(r" - ", "-")
            types.append(cls.type_.get(text, "plant_part"))

        for token in ent:
            token._.flag = "part"

            if token._.term == "part_term":
                cls.append_frag(token, frags)

            elif token._.term == "missing":
                cls.append_frag(token, frags)
                missing = True

            elif token._.term == "part_and":
                frags.append([])

        if any(t != types[0] for t in types):
            types[0] = "plant_part"

        all_parts = [" ".join(f) for f in frags]
        all_parts = [p.replace(r" - ", "-") for p in all_parts]
        all_parts = [cls.replace.get(p, p) for p in all_parts]
        part = all_parts[0] if len(all_parts) == 1 else all_parts

        trait = cls.from_ent(ent, part=part, type=types[0], missing=missing)

        ent[0]._.trait = trait
        return trait


@registry.misc("part_match")
def part_match(ent):
    return Part.part_match(ent)
