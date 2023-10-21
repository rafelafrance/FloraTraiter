from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
from typing import Optional

import regex as re
from spacy.language import Language
from spacy.util import registry
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes import reject_match
from traiter.pylib.traits import terms as t_terms
from traiter.pylib.traits.base import Base


@dataclass
class Name(Base):
    # Class vars ----------
    all_csvs: ClassVar[list[Path]] = [
        Path(__file__).parent / "terms" / "person_terms.csv",
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

    @classmethod
    def pipe(cls, nlp: Language, overwrite: Optional[list[str]] = None):
        add.term_pipe(nlp, name="person_terms", path=cls.all_csvs)

        overwrite = overwrite if overwrite else []

        add.trait_pipe(nlp, name="not_name_patterns", compiler=cls.not_name_patterns())

        add.trait_pipe(
            nlp,
            name="name_patterns",
            compiler=cls.name_patterns(),
            overwrite=overwrite + "name_prefix name_suffix".split(),
        )

        add.trait_pipe(
            nlp,
            name="double_name_patterns",
            compiler=cls.double_name_patterns(),
            overwrite=overwrite + "name name_prefix name_suffix".split(),
        )

        add.cleanup_pipe(nlp, name="name_cleanup")

    @classmethod
    def not_name_patterns(cls):
        decoder = {
            "acc_label": {"ENT_TYPE": "acc_label"},
            "id1": {"LOWER": {"REGEX": r"^(\w*\d+\w*)$"}},
            "id2": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
            "no_space": {"SPACY": False},
            "bad_name": {"ENT_TYPE": "not_name"},
            "bad_prefix": {"ENT_TYPE": "not_name_prefix"},
            "bad_suffix": {"ENT_TYPE": "not_name_suffix"},
            "shape": {"SHAPE": {"IN": t_const.NAME_AND_UPPER}},
        }
        return [
            Compiler(
                label="not_name",
                on_match="not_name_match",
                decoder=decoder,
                patterns=[
                    " bad_name+ ",
                    " bad_prefix+ ",
                    " bad_suffix+ ",
                    " shape+ bad_suffix+ ",
                    " bad_prefix+ shape+ ",
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
            "A": {"TEXT": {"REGEX": r"^[A-Z][A-Z]?[._,]?$"}},
            "_": {"TEXT": {"REGEX": r"^[._,]+$"}},
            "ambig": {"ENT_TYPE": {"IN": ["us_county", "color"]}},
            "and": {"LOWER": {"IN": cls.and_}},
            "dr": {"ENT_TYPE": "name_prefix"},
            "id1": {"LOWER": {"REGEX": r"^(\w*\d+\w*)$"}},
            "id2": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
            "jr": {"ENT_TYPE": "name_suffix"},
            "shape": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
            "shape4": {"SHAPE": {"IN": cls.name4}},
            "no_label": {"ENT_TYPE": "no_label"},
            "no_space": {"SPACY": False},
            "pre": {"ENT_TYPE": "last_prefix"},
            "upper": {"SHAPE": {"IN": t_const.UPPER_SHAPES}},
            "upper4": {"SHAPE": {"IN": cls.upper4}},
        }
        return [
            Compiler(
                label="name",
                on_match="name_match",
                decoder=decoder,
                patterns=[
                    "       shape  -? shape? -? pre? pre?   shape4",
                    "       shape  -? shape? -? pre? pre?   shape4   _? jr+",
                    "       shape  -? shape? -?   ambig",
                    "       shape  -? shape? -?   ambig   _? jr+",
                    "       ambig  -? shape? -? pre? pre?  shape4 ",
                    "       ambig  -? shape? -? pre? pre?  shape4   _? jr+",
                    "       A A? A?             pre? pre? shape4",
                    "       A A? A?             pre? pre? shape4   _? jr+",
                    "       shape A A? A?       pre? pre? shape4",
                    "       shape A A? A?       pre? pre? shape4   _? jr+",
                    "       shape ..             shape4",
                    "       shape ..             shape4   _? jr+",
                    "       shape ( shape )      shape4",
                    "       shape ( shape )      shape4   _? jr+",
                    "       shape ( shape )      shape4",
                    "dr+ _? shape  -? shape? -?  shape4",
                    "dr+ _? shape  -? shape? -?  shape4   _? jr+",
                    "dr+ _? shape  -? shape? -?  ambig",
                    "dr+ _? shape  -? shape? -?  ambig   _? jr+",
                    "dr+ _? ambig -? shape?  -?  shape4",
                    "dr+ _? ambig -? shape?  -?  shape4   _? jr+",
                    "dr+ _? A A? A?              shape4",
                    "dr+ _? A A? A?              shape4   _? jr+",
                    "dr+ _? shape A A? A?        shape4",
                    "dr+ _? shape A A? A?        shape4   _? jr+",
                    "dr+ _? shape ..             shape4",
                    "dr+ _? shape ..             shape4   _? jr+",
                    "dr+ _? shape ( shape )      shape4",
                    "dr+ _? shape ( shape )      shape4   _? jr+",
                    "dr+ _? shape ( shape )      shape4",
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
            "shape": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
            "shape4": {"SHAPE": {"IN": cls.name4}},
            "name": {"ENT_TYPE": "name"},
            "no_space": {"SPACY": False},
            "upper": {"SHAPE": {"IN": t_const.UPPER_SHAPES}},
            "upper4": {"SHAPE": {"IN": cls.upper4}},
        }
        return [
            Compiler(
                label="name",
                on_match="double_name_match",
                decoder=decoder,
                patterns=[
                    " shape and name+",
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
