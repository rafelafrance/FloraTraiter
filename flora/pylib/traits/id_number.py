from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import regex as re
from spacy.language import Language
from spacy.util import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits.base import Base


@dataclass(eq=False)
class IdNumber(Base):
    # Class vars ----------
    id_num_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "id_num_terms.csv"
    punct = "[.:;,_-]"
    # ---------------------

    id_num: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(id_number=self.id_num)

    @property
    def key(self) -> str:
        return self.key_builder("id_number")

    @classmethod
    def pipe(cls, nlp: Language = None):
        add.term_pipe(nlp, name="id_num_terms", path=cls.id_num_csv)

        add.trait_pipe(
            nlp,
            name="id_num_patterns",
            compiler=cls.id_num_patterns(),
            overwrite=["num_label"],
        )

        add.cleanup_pipe(nlp, name="id_num_cleanup")

    @classmethod
    def id_num_patterns(cls):
        decoder = {
            "-": {"TEXT": {"REGEX": r"^[._-]+$"}},
            ":": {"LOWER": {"REGEX": rf"^(by|{cls.punct}+)$"}},
            "acc_label": {"ENT_TYPE": "acc_label"},
            "id1": {"LOWER": {"REGEX": r"^(\w*\d+\w*)$"}},
            "id2": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
            "num_label": {"ENT_TYPE": "num_label"},
            "no_space": {"SPACY": False},
        }
        return [
            Compiler(
                label="id_num",
                on_match="id_num_match",
                keep=["id_num"],
                decoder=decoder,
                patterns=[
                    "id1+ no_space+ id1",
                    "id1+ no_space+ id2",
                    "id1",
                    "num_label+ :* id1? no_space? id1? -? id2",
                ],
            ),
            Compiler(
                label="not_id_num",
                on_match="not_id_num_match",
                decoder=decoder,
                patterns=[
                    "acc_label+ id1+ no_space+ id1",
                    "acc_label+ id1+ no_space+ id2",
                    "acc_label+ id1",
                ],
            ),
        ]

    @classmethod
    def id_num_match(cls, ent):
        frags = [t.text for t in ent if t.ent_type_ != "num_label"]
        id_num = "".join(frags)
        id_num = re.sub(r"^[,]", "", id_num)
        trait = cls.from_ent(ent, id_num=id_num)
        ent[0]._.trait = trait
        ent[0]._.flag = "id_num"
        return trait

    @classmethod
    def not_id_num_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("id_num_match")
def id_num_match(ent):
    return IdNumber.id_num_match(ent)


@registry.misc("not_id_num_match")
def not_id_num_match(ent):
    return IdNumber.not_id_num_match(ent)
