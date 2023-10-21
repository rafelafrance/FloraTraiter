import re
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes.reject_match import REJECT_MATCH

from .linkable import Linkable


@dataclass
class Part(Linkable):
    # Class vars ----------
    part_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "part_terms.csv"
    missing_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "missing_terms.csv"
    all_csvs: ClassVar[list[Path]] = [part_csv, missing_csv]

    replace: ClassVar[dict[str, str]] = term_util.term_data(all_csvs, "replace")
    type_: ClassVar[dict[str, str]] = term_util.term_data(part_csv, "type")

    other_labels: ClassVar[list[str]] = "missing_part multiple_parts".split()
    all_labels: ClassVar[list[str]] = ["part", *other_labels]
    # ---------------------

    part: str | list[str] = None
    type: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="part_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="part_patterns",
            compiler=cls.part_patterns(),
            overwrite=""" part part_and part_leader part_missing """.split(),
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
            "part": {"ENT_TYPE": "part"},
        }

        return [
            Compiler(
                label="part",
                id="part",
                on_match="part_match",
                keep="part",
                decoder=decoder,
                patterns=[
                    "leader? part+",
                    "leader? part+ - part+",
                ],
            ),
            Compiler(
                label="missing_part",
                on_match="part_match",
                keep="missing_part",
                decoder=decoder,
                patterns=[
                    "missing part+",
                    "missing part+ and part+",
                    "missing part+ -   part+",
                ],
            ),
            Compiler(
                label="multiple_parts",
                on_match="part_match",
                keep="multiple_parts",
                decoder=decoder,
                patterns=[
                    "leader? part+ and part+",
                    "missing part+ and part+",
                ],
            ),
            Compiler(
                label="not_a_part",
                on_match=REJECT_MATCH,
                decoder=decoder,
                patterns=[
                    "- part+",
                    "bad_part",
                ],
            ),
        ]

    @classmethod
    def part_match(cls, ent):
        frags = [[]]
        label = ent.label_
        relabel = ent.label_

        for token in ent:
            token._.flag = "part"

            if relabel not in cls.other_labels and token._.term == "part":
                relabel = token._.term

            if token._.term in cls.all_labels:
                part = cls.replace.get(token.lower_, token.lower_)

                if part not in frags[-1]:
                    frags[-1].append(part)

                if label not in ("missing_part", "multiple_parts", "subpart"):
                    label = token._.term

            elif token._.term == "missing":
                frags[-1].append(cls.replace.get(token.lower_, token.lower_))

            elif token._.term == "part_and":
                frags.append([])

        all_parts = [" ".join(f) for f in frags]
        all_parts = [re.sub(r" - ", "-", p) for p in all_parts]
        all_parts = [cls.replace.get(p, p) for p in all_parts]
        part = all_parts[0] if len(all_parts) == 1 else all_parts

        type_ = None if isinstance(part, list) else cls.type_.get(part, part)

        trait = cls.from_ent(ent, part=part, type=type_)

        ent[0]._.trait = trait
        return trait


@registry.misc("part_match")
def part_match(ent):
    return Part.part_match(ent)
