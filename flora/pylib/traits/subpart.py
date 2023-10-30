from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from .linkable import Linkable


@dataclass
class Subpart(Linkable):
    # Class vars ----------
    all_csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "subpart_terms.csv",
        Path(__file__).parent / "terms" / "part_terms.csv",
        Path(__file__).parent / "terms" / "missing_terms.csv",
    ]

    replace = term_util.term_data(all_csvs, "replace")
    # ---------------------

    # subpart in base class
    missing: bool = None

    def to_dwc(self, dwc, ent):
        dwc.new_rec()
        prepend = "missing" if self.missing else ""
        key = self.dwc_key(prepend=prepend)
        dwc.add_dyn(**{key: self.subpart})

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="subpart_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="subpart_patterns",
            compiler=cls.subpart_patterns(),
            overwrite=["part", "part_leader", "missing", "subpart"],
        )
        add.cleanup_pipe(nlp, name="subpart_cleanup")

    @classmethod
    def subpart_patterns(cls):
        return [
            Compiler(
                label="subpart",
                on_match="subpart_match",
                keep="subpart",
                decoder={
                    ",": {"TEXT": {"IN": t_const.COMMA}},
                    "-": {"TEXT": {"IN": t_const.DASH}, "OP": "+"},
                    "leader": {"ENT_TYPE": "part_leader"},
                    "missing": {"ENT_TYPE": "missing"},
                    "part": {"ENT_TYPE": "part"},
                    "subpart": {"ENT_TYPE": "subpart"},
                },
                patterns=[
                    "leader* ,? leader* subpart+",
                    "leader* ,? leader* subpart+ - subpart+",
                    "leader* ,? leader* part+ -?   subpart+",
                    "- subpart+",
                    "missing part+ -? subpart+",
                    "missing subpart+",
                ],
            ),
        ]

    @classmethod
    def subpart_match(cls, ent):
        frags = {}
        missing = None

        for token in ent:
            if token._.term in ("subpart", "part"):
                frag = cls.replace.get(token.lower_, token.lower_)
                frags[frag] = 1

            elif token._.term == "missing":
                frag = cls.replace.get(token.lower_, token.lower_)
                frags[frag] = 1
                missing = True

        subpart = " ".join(frags.keys()).replace(" - ", "-")
        subpart = cls.replace.get(subpart, subpart)

        return cls.from_ent(ent, subpart=subpart, missing=missing)


@registry.misc("subpart_match")
def subpart_match(ent):
    return Subpart.subpart_match(ent)
