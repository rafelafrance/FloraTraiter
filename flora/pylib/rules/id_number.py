from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib import term_util as tu
from traiter.pylib.darwin_core import DWC, DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class IdNumber(Base):
    # Class vars ----------
    id_num_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "id_num_terms.csv"
    punct: ClassVar[str] = "[.:;,_-]"
    labels: ClassVar[list[str]] = tu.get_labels(id_num_csv)
    # ---------------------

    number: str = None
    type: str = None
    has_label: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        if self.key.startswith(DWC):
            return dwc.add(**{self.key: self.number})
        return dwc.add_dyn(**{self.key: self.number})

    @property
    def key(self) -> str:
        match self.type:
            case "accession_number":
                key = "accessionNumber"
            case "collector_id":
                key = DarwinCore.ns("recordedByID")
            case _:
                key = DarwinCore.ns("recordNumber")
        return key

    @classmethod
    def pipe(cls, nlp: Language = None):
        add.term_pipe(nlp, name="id_num_terms", path=cls.id_num_csv)
        # add.debug_tokens(nlp)  # ################################################

        add.trait_pipe(
            nlp,
            name="not_id_num_patterns",
            compiler=cls.not_id_num_patterns(),
        )

        add.trait_pipe(
            nlp,
            name="id_num_patterns",
            compiler=cls.id_num_patterns(),
            overwrite=cls.labels,
        )
        # add.debug_tokens(nlp)  # ################################################

        add.cleanup_pipe(nlp, name="id_num_cleanup", delete=["not_id_number"])

    @classmethod
    def not_id_num_patterns(cls):
        decoder = {
            "-": {"TEXT": {"REGEX": r"^[._-]+$"}},
            ":": {"LOWER": {"REGEX": rf"^(by|{cls.punct}+)$"}},
            "bad_prefix": {"ENT_TYPE": {"IN": ["not_id_prefix", "not_id"]}},
            "bad_suffix": {"ENT_TYPE": {"IN": ["not_id_suffix", "not_id"]}},
            "id1": {"LOWER": {"REGEX": r"^(\w*\d+\w*)$"}},
            "id2": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
            "label": {"ENT_TYPE": {"IN": cls.labels}},
            "no_space": {"SPACY": False},
            "bad_leader": {"LOWER": {"REGEX": r"^[rs]\d{2,3}$"}},
            "bad_follower": {"LOWER": {"REGEX": r"^[nesw]$"}},
        }
        return [
            Compiler(
                label="not_id_number",
                keep="not_id_number",
                on_match="not_id_number_match",
                decoder=decoder,
                patterns=[
                    "bad_prefix+ id1+ no_space+ id1",
                    "bad_prefix+ id1+ no_space+ id2",
                    "bad_prefix+ id1",
                    "bad_prefix+ id1+ no_space+ id1 bad_suffix+",
                    "bad_prefix+ id1+ no_space+ id2 bad_suffix+",
                    "bad_prefix+ id1                bad_suffix+",
                    "            id1+ no_space+ id1 bad_suffix+",
                    "            id1+ no_space+ id2 bad_suffix+",
                    "            id1                bad_suffix+",
                    " bad_leader bad_follower",
                ],
            ),
        ]

    @classmethod
    def id_num_patterns(cls):
        decoder = {
            "-": {"TEXT": {"REGEX": r"^[._-]+$"}},
            ":": {"LOWER": {"REGEX": rf"^(by|{cls.punct}+)$"}},
            "id1": {"LOWER": {"REGEX": r"^(\w*\d+\w*)$"}},
            "id2": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
            "label": {"ENT_TYPE": {"IN": cls.labels}},
            "no_space": {"SPACY": False},
        }
        return [
            Compiler(
                label="id_number",
                on_match="id_number_match",
                keep="id_number",
                decoder=decoder,
                patterns=[
                    "id1+ no_space+ id1",
                    "id1+ no_space+ id2",
                    "id1",
                    "label+ :* id1? no_space? id1? -? id2",
                    "label+ :* id1+ no_space+ id1",
                    "label+ :* id1+ no_space+ id2",
                    "label+ :* id1",
                ],
            ),
        ]

    @classmethod
    def id_number_match(cls, ent):
        frags = []
        type_ = None
        has_label = None

        for token in ent:
            if token.ent_type_ == "not_id_num":
                raise reject_match.RejectMatch

            elif token.ent_type_ in cls.labels:
                type_ = token.ent_type_
                has_label = True

            else:
                frags.append(token.text)

        id_num = "".join(frags)
        type_ = type_ if type_ else "record_number"

        return cls.from_ent(ent, number=id_num, type=type_, has_label=has_label)

    @classmethod
    def not_id_number_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("not_id_number_match")
def not_id_number_match(ent):
    return IdNumber.not_id_number_match(ent)


@registry.misc("id_number_match")
def id_number_match(ent):
    return IdNumber.id_number_match(ent)
