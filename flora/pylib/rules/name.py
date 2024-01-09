from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import regex as re
from spacy.language import Language
from spacy.util import registry
from traiter.pylib import const as t_const
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.rules import terms as t_terms
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class Name(Base):
    # Class vars ----------
    all_csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "id_num_terms.csv",
        Path(__file__).parent / "terms" / "job_terms.csv",
        Path(t_terms.__file__).parent / "name_terms.csv",
    ]

    and_: ClassVar[list[str]] = ["and", "&"]
    punct: ClassVar[list[str]] = "[.:;,_-]"
    sep: ClassVar[list[str]] = ["and", "with", "et", *list("&._,;")]
    conj: ClassVar[list[str]] = ["CCONJ", "ADP"]

    name4: ClassVar[list[str]] = [
        s for s in t_const.NAME_SHAPES if len(s) >= 4 and s[-1].isalpha()
    ]
    upper4: ClassVar[list[str]] = [
        s for s in t_const.UPPER_SHAPES if len(s) >= 4 and s[-1].isalpha()
    ]

    temp = "".join(t_const.OPEN + t_const.CLOSE + t_const.QUOTE + list(".,'&"))
    name_re: ClassVar[re] = re.compile(rf"^[\sa-z{re.escape(temp)}-]+$")
    # ---------------------

    name: str | list[str] = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(name=self.name)

    @property
    def key(self) -> str:
        return "name"

    @classmethod
    def pipe(cls, nlp: Language, overwrite: list[str] | None = None):
        add.term_pipe(nlp, name="name_terms", path=cls.all_csvs)

        overwrite = overwrite if overwrite else []

        add.trait_pipe(nlp, name="not_name_patterns", compiler=cls.not_name_patterns())

        # add.debug_tokens(nlp)  # ################################################
        add.trait_pipe(
            nlp,
            name="name_patterns",
            compiler=cls.name_patterns(),
            overwrite=overwrite + "name_prefix name_suffix".split(),
        )
        # add.debug_tokens(nlp)  # ################################################

        add.trait_pipe(
            nlp,
            name="double_name_patterns",
            compiler=cls.double_name_patterns(),
            overwrite=overwrite + "name name_prefix name_suffix".split(),
        )
        # add.debug_tokens(nlp)  # ################################################

        add.cleanup_pipe(nlp, name="name_cleanup", delete=["not_name"])

    @classmethod
    def not_name_patterns(cls):
        decoder = {
            "job_label": {"ENT_TYPE": "job_label"},
            "no_space": {"SPACY": False},
            "bad_name": {"ENT_TYPE": "not_name"},
            "bad_prefix": {"ENT_TYPE": "not_name_prefix"},
            "bad_suffix": {"ENT_TYPE": "not_name_suffix"},
            "shape": {"SHAPE": {"IN": t_const.NAME_AND_UPPER}},
        }
        return [
            Compiler(
                label="not_name",
                keep="not_name",
                on_match="not_name_match",
                decoder=decoder,
                patterns=[
                    " bad_name+ ",
                    " bad_prefix+ ",
                    " bad_suffix+ ",
                    " shape+ bad_suffix+ ",
                    " bad_prefix+ shape+ ",
                    " job_label+ ",
                ],
            ),
        ]

    @classmethod
    def name_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN + t_const.QUOTE}},
            ")": {"TEXT": {"IN": t_const.CLOSE + t_const.QUOTE}},
            ",": {"TEXT": {"IN": t_const.COMMA}},
            "-": {"TEXT": {"REGEX": r"^[._-]+$"}},
            "..": {"TEXT": {"REGEX": r"^[.]+$"}},
            ":": {"LOWER": {"REGEX": rf"^(by|{cls.punct}+)$"}},
            "A": {"TEXT": {"REGEX": r"^[A-Z][._,]?[A-Z]?[._,]?$"}},
            "_": {"TEXT": {"REGEX": r"^[._,]+$"}},
            "ambig": {"ENT_TYPE": {"IN": ["us_county", "color"]}},
            "and": {"LOWER": {"IN": cls.and_}},
            "dr": {"ENT_TYPE": "name_prefix"},
            "jr": {"ENT_TYPE": "name_suffix"},
            "mix": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
            "mix4": {"SHAPE": {"IN": cls.name4}},
            "num_label": {"ENT_TYPE": "num_label"},
            "no_space": {"SPACY": False},
            "pre": {"ENT_TYPE": "last_prefix"},
            "upper": {"SHAPE": {"IN": t_const.UPPER_SHAPES}},
            "upper4": {"SHAPE": {"IN": cls.upper4}},
        }
        return [
            Compiler(
                label="name",
                keep="name",
                on_match="name_match",
                decoder=decoder,
                patterns=[
                    "       mix  -?   mix? -?  pre? pre?   mix4",
                    "       mix  -?   mix? -?  pre? pre?   mix4   _? jr+",
                    "       mix  -?   mix? -?  ambig",
                    "       mix  -?   mix? -?  ambig   _? jr+",
                    "       mix  -? mix? -?  pre? pre?  ambig ",
                    "       mix  -? mix? -?  pre? pre?  ambig   _? jr+",
                    "       A A? A?            pre? pre? mix4",
                    "       A A? A?            pre? pre? mix4   _? jr+",
                    "       mix A A? A?        pre? pre? mix4",
                    "       mix A A? A?        pre? pre? mix4   _? jr+",
                    "       mix ..             mix4",
                    "       mix ..             mix4   _? jr+",
                    "       mix ( mix )        mix4",
                    "       mix ( mix )        mix4   _? jr+",
                    "       mix ( mix )        mix4",
                    "       mix ( mix ) A A? A? mix4",
                    "dr+ _? mix  -? mix? -?    mix4",
                    "dr+ _? mix  -? mix? -?    mix4   _? jr+",
                    "dr+ _? mix  -? mix? -?    ambig",
                    "dr+ _? mix  -? mix? -?    ambig   _? jr+",
                    "dr+ _? mix -? mix?  -?  ambig",
                    "dr+ _? mix -? mix?  -?  ambig   _? jr+",
                    "dr+ _? A A? A?            mix4",
                    "dr+ _? A A? A?            mix4   _? jr+",
                    "dr+ _? mix A A? A?        mix4",
                    "dr+ _? mix A A? A?        mix4   _? jr+",
                    "dr+ _? mix ..             mix4",
                    "dr+ _? mix ..             mix4   _? jr+",
                    "dr+ _? mix ( mix )        mix4",
                    "dr+ _? mix ( mix )        mix4   _? jr+",
                    "dr+ _? mix ( mix )        mix4",
                    "dr+ _? mix ( mix ) A A? A? mix4",
                    "       upper  -? upper? -? pre? pre?   upper4",
                    "       upper  -? upper? -? pre? pre?   upper4   _? jr+",
                    "       upper  -? upper? -?   ambig",
                    "       upper  -? upper? -?   ambig   _? jr+",
                    "       A A? A?      pre? pre? upper4",
                    "       A A? A?      pre? pre? upper4   _? jr+",
                    "       upper A A? A? pre? pre? upper4",
                    "       upper A A? A? pre? pre? upper4   _? jr+",
                    "       upper ..         upper4",
                    "       upper ..         upper4   _? jr+",
                    "       upper ( upper )  upper4",
                    "       upper ( upper )  upper4   _? jr+",
                    "       upper ( upper )  upper4",
                ],
            ),
        ]

    @classmethod
    def double_name_patterns(cls):
        decoder = {
            "A": {"TEXT": {"REGEX": r"^[A-Z][A-Z]?[._,]?$"}},
            "ambig": {"ENT_TYPE": {"IN": ["us_county", "color"]}},
            "and": {"LOWER": {"IN": cls.and_}},
            "mix": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
            "mix4": {"SHAPE": {"IN": cls.name4}},
            "name": {"ENT_TYPE": "name"},
            "no_space": {"SPACY": False},
            "upper": {"SHAPE": {"IN": t_const.UPPER_SHAPES}},
            "upper4": {"SHAPE": {"IN": cls.upper4}},
        }
        return [
            Compiler(
                label="name",
                keep="name",
                on_match="double_name_match",
                decoder=decoder,
                patterns=[
                    " mix and name+",
                ],
            ),
        ]

    @classmethod
    def name_match(cls, ent):
        name = ent.text
        name = re.sub(rf" ({cls.punct})", r"\1", name)
        name = re.sub(r"\.\.|_", "", name)

        if not cls.name_re.match(name.lower()):
            raise reject_match.RejectMatch

        for token in ent:
            token._.flag = "skip"

            # If there's a digit in the name reject it
            if re.search(r"\d", token.text):
                raise reject_match.RejectMatch

            # If it is all lower case reject it
            if (
                token.text.islower()
                and token.ent_type_ != "last_prefix"
                and token.lower_ not in cls.and_
            ):
                raise reject_match.RejectMatch

        trait = cls.from_ent(ent, name=name)
        ent[0]._.trait = trait
        ent[0]._.flag = "name"
        return trait

    @classmethod
    def double_name_match(cls, ent):
        if ent[0].ent_type_ == "name":
            raise reject_match.RejectMatch

        trait = cls.from_ent(ent, name=ent.text)

        for token in ent:
            token._.flag = "skip"

        ent[0]._.trait = trait
        ent[0]._.flag = "name"
        return trait

    @classmethod
    def not_name_match(cls, ent):
        return cls.from_ent(ent)


@registry.misc("not_name_match")
def not_name_match(ent):
    return Name.not_name_match(ent)


@registry.misc("name_match")
def name_match(ent):
    return Name.name_match(ent)


@registry.misc("double_name_match")
def double_name_match(ent):
    return Name.double_name_match(ent)
