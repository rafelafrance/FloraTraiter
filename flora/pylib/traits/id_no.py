from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import regex as re
from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits.base import Base


@dataclass
class IdNo(Base):
    # Class vars ----------
    id_no_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "person_terms.csv"
    punct = "[.:;,_-]"
    # ---------------------

    id_no: str = None

    @classmethod
    def pipe(cls, nlp: Language = None):
        add.term_pipe(nlp, name="id_no_terms", path=cls.id_no_csv)

        add.trait_pipe(
            nlp,
            name="id_no_patterns",
            compiler=cls.id_no_patterns(),
            overwrite=["no_label"],
        )

        add.cleanup_pipe(nlp, name="id_no_cleanup")

    @classmethod
    def id_no_patterns(cls):
        decoder = {
            "-": {"TEXT": {"REGEX": r"^[._-]+$"}},
            ":": {"LOWER": {"REGEX": rf"^(by|{cls.punct}+)$"}},
            "id1": {"LOWER": {"REGEX": r"^(\w*\d+\w*)$"}},
            "id2": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
            "no_label": {"ENT_TYPE": "no_label"},
            "no_space": {"SPACY": False},
        }
        return [
            Compiler(
                label="id_no",
                on_match="id_no_match",
                decoder=decoder,
                patterns=[
                    "id1+ no_space+ id1",
                    "id1+ no_space+ id2",
                    "id1",
                    "no_label+ :* id1? no_space? id1? -? id2",
                ],
            ),
            Compiler(
                label="not_id_no",
                on_match="not_id_no_match",
                decoder=decoder,
                patterns=[
                    "acc_label+ id1+ no_space+ id1",
                    "acc_label+ id1+ no_space+ id2",
                    "acc_label+ id1",
                ],
            ),
        ]

    @classmethod
    def id_no_match(cls, ent):
        frags = [t.text for t in ent if t.ent_type_ != "no_label"]
        id_no = "".join(frags)
        id_no = re.sub(r"^[,]", "", id_no)
        trait = cls.from_ent(ent, id_no=id_no)
        ent[0]._.trait = trait
        ent[0]._.flag = "id_no"
        return trait

    @classmethod
    def not_id_no_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("id_no_match")
def id_no_match(ent):
    return IdNo.id_no_match(ent)


@registry.misc("not_id_no_match")
def not_id_no_match(ent):
    return IdNo.not_id_no_match(ent)
