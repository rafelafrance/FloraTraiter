from collections import namedtuple
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import regex as re
from spacy.language import Language
from spacy.util import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import ACCUMULATOR
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes import reject_match
from traiter.pylib.pipes import trait as t_trait
from traiter.pylib.traits import terms as t_terms

from flora.pylib.traits import terms as f_terms

from .base import Base

PERSON_CSV = Path(__file__).parent / "terms" / "person_terms.csv"
NAME_CSV = Path(t_terms.__file__).parent / "name_terms.csv"
JOB_CSV = Path(f_terms.__file__).parent / "job_terms.csv"
ALL_CSVS = [PERSON_CSV, NAME_CSV, JOB_CSV]

REPLACE = term_util.term_data(JOB_CSV, "replace")
REPLACE = {"".join(k.split()): v for k, v in REPLACE.items()}

AND = ["and", "&"]
PUNCT = "[.:;,_-]"
SEP = ["and", "with", "et", *list("&._,;")]
CONJ = ["CCONJ", "ADP"]

NAME4 = [s for s in t_const.NAME_SHAPES if len(s) >= 4 and s[-1].isalpha()]
UPPER4 = [s for s in t_const.UPPER_SHAPES if len(s) >= 4 and s[-1].isalpha()]

NAME_RE = "".join(t_const.OPEN + t_const.CLOSE + t_const.QUOTE + list(".,'&"))
NAME_RE = re.compile(rf"^[\sa-z{re.escape(NAME_RE)}-]+$")

Separated = namedtuple("Separated", "idx ent")


def build(nlp: Language, overwrite: Optional[list[str]] = None):
    add.term_pipe(nlp, name="person_terms", path=ALL_CSVS)

    overwrite = overwrite if overwrite else []

    add.trait_pipe(nlp, name="not_name_patterns", compiler=not_name_patterns())

    add.trait_pipe(
        nlp,
        name="name_patterns",
        compiler=name_patterns(),
        overwrite=overwrite + "name_prefix name_suffix no_label".split(),
        keep=[*ACCUMULATOR.keep, "job_label", "no_label", "not_name", "not_id_no"],
    )

    add.trait_pipe(
        nlp,
        name="double_name_patterns",
        compiler=double_name_patterns(),
        overwrite=overwrite + "name name_prefix name_suffix no_label".split(),
        keep=[*ACCUMULATOR.keep, "job_label", "no_label", "not_name", "not_id_no"],
    )

    job_overwrite = overwrite + """name job_label no_label id_no""".split()
    add.trait_pipe(
        nlp,
        name="job_patterns",
        compiler=job_patterns(),
        overwrite=job_overwrite,
        keep=[*ACCUMULATOR.keep, "not_name", "not_id_no"],
    )

    add.trait_pipe(
        nlp,
        name="other_patterns",
        compiler=other_patterns(),
        overwrite=job_overwrite,
        keep=[*ACCUMULATOR.keep, "not_name", "not_id_no"],
    )

    add.custom_pipe(nlp, registered="separated_collector")

    add.trait_pipe(
        nlp,
        name="extend_names",
        compiler=extend_name_patterns(),
        overwrite=["job"],
        keep=[*ACCUMULATOR.keep, "not_name", "not_id_no"],
    )

    add.custom_pipe(nlp, registered="name_only")

    add.trait_pipe(
        nlp,
        name="job_rename",
        compiler=job_rename_patterns(),
        overwrite=["other_collector", "extend_names"],
    )

    add.cleanup_pipe(nlp, name="person_cleanup")


def not_name_patterns():
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


def name_patterns():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN + t_const.QUOTE}},
        ")": {"TEXT": {"IN": t_const.CLOSE + t_const.QUOTE}},
        ",": {"TEXT": {"IN": t_const.COMMA}},
        "-": {"TEXT": {"REGEX": r"^[._-]+$"}},
        "..": {"TEXT": {"REGEX": r"^[.]+$"}},
        ":": {"LOWER": {"REGEX": rf"^(by|{PUNCT}+)$"}},
        "A": {"TEXT": {"REGEX": r"^[A-Z][A-Z]?[._,]?$"}},
        "_": {"TEXT": {"REGEX": r"^[._,]+$"}},
        "ambig": {"ENT_TYPE": {"IN": ["us_county", "color"]}},
        "and": {"LOWER": {"IN": AND}},
        "dr": {"ENT_TYPE": "name_prefix"},
        "id1": {"LOWER": {"REGEX": r"^(\w*\d+\w*)$"}},
        "id2": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
        "jr": {"ENT_TYPE": "name_suffix"},
        "shape": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
        "shape4": {"SHAPE": {"IN": NAME4}},
        "no_label": {"ENT_TYPE": "no_label"},
        "no_space": {"SPACY": False},
        "pre": {"ENT_TYPE": "last_prefix"},
        "upper": {"SHAPE": {"IN": t_const.UPPER_SHAPES}},
        "upper4": {"SHAPE": {"IN": UPPER4}},
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
    ]


def double_name_patterns():
    decoder = {
        "A": {"TEXT": {"REGEX": r"^[A-Z][A-Z]?[._,]?$"}},
        "ambig": {"ENT_TYPE": {"IN": ["us_county", "color"]}},
        "and": {"LOWER": {"IN": AND}},
        "shape": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
        "shape4": {"SHAPE": {"IN": NAME4}},
        "name": {"ENT_TYPE": "name"},
        "no_space": {"SPACY": False},
        "upper": {"SHAPE": {"IN": t_const.UPPER_SHAPES}},
        "upper4": {"SHAPE": {"IN": UPPER4}},
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


def job_patterns():
    return [
        Compiler(
            label="job",
            on_match="job_match",
            keep="job",
            decoder={
                ":": {"LOWER": {"REGEX": rf"^(by|{PUNCT}+)$"}},
                ",": {"LOWER": {"REGEX": rf"^({PUNCT}+)$"}},
                "and": {"POS": {"IN": CONJ}},
                "bad": {"ENT_TYPE": {"IN": ["month"]}},
                "by": {"LOWER": {"IN": ["by"]}},
                "job_label": {"ENT_TYPE": "job_label"},
                "id_no": {"ENT_TYPE": {"IN": ["id_no", "labeled_id_no"]}},
                "maybe": {"POS": "PROPN"},
                "name": {"ENT_TYPE": "name"},
                "nope": {"ENT_TYPE": "not_name"},
                "sep": {"LOWER": {"IN": SEP}},
                "sp": {"IS_SPACE": True},
            },
            patterns=[
                "job_label+ :* sp? name+",
                "job_label+ :* sp? name+ sep sp? name+",
                "job_label+ :* sp? name+ sep sp? name+ sep sp? name+",
                "job_label+ :* sp? name+                             ,* sp? id_no+",
                "job_label+ :* sp? name+ sep sp? name+               ,* sp? id_no+",
                "job_label+ :* sp? name+ sep sp? name+ sep sp? name+ ,* sp? id_no+",
                "                  name+                             ,* sp? id_no+",
                "                  name+ sep sp? name+               ,* sp? id_no+",
                "                  name+ sep sp? name+ sep sp? name+ ,* sp? id_no+",
                "id_no+        sp? name+",
                "id_no+        sp? name+ sep sp? name+",
                "id_no+        sp? name+ sep sp? name+ sep sp? name+",
                "job_label+ :* sp? name+ sep sp? name+ sep sp? name+ sep sp? name+",
                "job_label+ :* maybe? name+",
                "job_label+ :* maybe? name+ and maybe? name+",
            ],
        ),
    ]


def other_patterns():
    decoder = {
        "other_label": {"ENT_TYPE": "other_label"},
        "name": {"ENT_TYPE": "name"},
        "sep": {"LOWER": {"IN": SEP}},
        "sp": {"IS_SPACE": True},
    }

    return [
        Compiler(
            label="other_collector",
            on_match="other_match",
            decoder=decoder,
            patterns=[
                "other_label+ sp? name+ ",
                "other_label+ sp? name+ sep* sp? name+ ",
                "other_label+ sp? name+ sep* sp? name+ sep* sp? name+ ",
                "other_label+ sp? name+ sep* sp? name+ sep* sp? name+ sep* sp? name+ ",
                (
                    "other_label+ sp? name+ sep* sp? name+ sep* sp? name+ sep* sp? "
                    "name+ sep* sp? name+"
                ),
                (
                    "other_label+ sp? name+ sep* sp? name+ sep* sp? name+ sep* sp? "
                    "name+ sep* sp? name+ sep* sp? name+"
                ),
            ],
        ),
    ]


def extend_name_patterns():
    decoder = {
        "and": {"POS": {"IN": CONJ}},
        "maybe": {"POS": "PROPN"},
        "name": {"ENT_TYPE": "name"},
        "other_collector": {"ENT_TYPE": "other_collector"},
        "sep": {"LOWER": {"IN": SEP}},
    }

    return [
        Compiler(
            label="extend_names",
            on_match="extend_names",
            decoder=decoder,
            patterns=[
                " other_collector+ sep* name+ ",
                " other_collector+ sep* maybe ",
                " other_collector+ sep* name  and name+ ",
                " other_collector+ sep* maybe and maybe maybe ",
            ],
        ),
    ]


def job_rename_patterns():
    return Compiler(
        label="job",
        keep="job",
        on_match="job_rename_match",
        decoder={
            "rename": {"ENT_TYPE": {"IN": ["other_collector", "extend_names"]}},
        },
        patterns=[
            "rename+",
        ],
    )


@dataclass()
class Name(Base):
    name: str | list[str] = None

    @classmethod
    def name_match(cls, ent):
        name = ent.text
        name = re.sub(rf" ({PUNCT})", r"\1", name)
        name = re.sub(r"\.\.|_", "", name)

        if not NAME_RE.match(name.lower()):
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
                and token.lower_ not in AND
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


@dataclass()
class IdNo(Base):
    id_no: str = None

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


@dataclass()
class Job(Base):
    job: str = None
    name: str | list[str] = None
    id_no: str = None

    @classmethod
    def job_match(cls, ent):
        job = []
        people = []
        id_no = None

        for token in ent:
            if token._.flag == "skip" or token.ent_type_ == "no_label":
                continue

            elif token.ent_type_ == "job_label":
                job.append(token.lower_)

            elif token._.flag == "name":
                people.append(token._.trait.name)

            elif token._.flag == "id_no":
                id_no = token._.trait.id_no

            token._.flag = "skip"

        if not people:
            raise reject_match.RejectMatch

        job = "".join(job)
        job = REPLACE.get(job, job)
        job = job if job else "collector"

        name = people if len(people) > 1 else people[0]

        trait = cls.from_ent(ent, name=name, id_no=id_no, job=job)

        ent[0]._.flag = job
        ent[0]._.trait = trait

        return trait

    @classmethod
    def other_match(cls, ent):
        people = []

        for token in ent:
            if token._.flag == "name":
                people.append(token._.trait.name)

            token._.flag = "skip"

        if not people:
            raise reject_match.RejectMatch

        name = people if len(people) > 1 else people[0]

        trait = cls.from_ent(ent, name=name, job="other_collector")

        ent[0]._.flag = "other_collector"
        ent[0]._.trait = trait

        return trait

    @classmethod
    def extend_names(cls, ent):
        data = {}
        people = []

        for token in ent:
            if token._.flag == "other_collector":
                data = asdict(token._.trait)
                names = token._.trait.name
                people += names if isinstance(names, list) else [names]

            elif token._.flag == "skip" or token.text in PUNCT:
                continue

            else:
                people.append(token.text)

        data["name"] = people
        data["job"] = "other_collector"

        trait = cls.from_ent(ent, **data)

        ent[0]._.flag = "other_collector"
        ent[0]._.trait = trait

        return trait

    @classmethod
    def job_rename_match(cls, ent):
        data = {}

        for token in ent:
            if token._.flag == "other_collector":
                data = asdict(token._.trait)

        ent._.relabel = "job"
        name = data["name"]
        data["name"] = name if len(name) > 1 else name[0]
        return cls.from_ent(ent, **data)


@registry.misc("not_name_match")
def not_name_match(ent):
    return Name.not_name_match(ent)


@registry.misc("name_match")
def name_match(ent):
    return Name.name_match(ent)


@registry.misc("double_name_match")
def double_name_match(ent):
    return Name.double_name_match(ent)


@registry.misc("id_no_match")
def id_no_match(ent):
    return IdNo.id_no_match(ent)


@registry.misc("not_id_no_match")
def not_id_no_match(ent):
    return IdNo.not_id_no_match(ent)


@registry.misc("job_match")
def job_match(ent):
    return Job.job_match(ent)


@registry.misc("other_match")
def other_match(ent):
    return Job.other_match(ent)


@registry.misc("extend_names")
def extend_names(ent):
    return Job.extend_names(ent)


@registry.misc("job_rename_match")
def job_rename_match(ent):
    return Job.job_rename_match(ent)


@Language.component("separated_collector")
def separated_collector(doc):
    """Look for collectors separated from their ID numbers."""
    name = None
    id_no = None

    for i, ent in enumerate(doc.ents):
        # Last name before an ID number
        if ent.label_ == "name" and not id_no:
            name = Separated(i, ent)

        # First ID number after a name
        elif ent.label_ == "id_no" and not id_no and name:
            id_no = Separated(i, ent)

    if name and id_no and id_no.idx - name.idx <= 5:
        t_trait.relabel_entity(name.ent, "job", relabel_tokens=True)
        t_trait.relabel_entity(id_no.ent, "job", relabel_tokens=True)

        name_t = name.ent._.trait
        id_no_t = id_no.ent._.trait

        data = {"job": "collector", "name": name_t.name, "id_no": id_no_t.id_no}
        name.ent._.trait = Job.from_ent(name.ent, **data)
        id_no.ent._.trait = Job.from_ent(id_no.ent, **data)

    return doc


@Language.component("name_only")
def name_only(doc):
    """Look for names next to a date."""
    for one, two in zip(doc.ents[:-1], doc.ents[1:]):
        if one.end != two.start:
            continue

        if one.label_ == "date" and two.label_ == "name":
            name_to_collector(two)

        elif one.label_ == "name" and two.label_ == "date":
            name_to_collector(one)

    return doc


def name_to_collector(ent):
    if not hasattr(ent._.trait, "name"):
        return
    t_trait.relabel_entity(ent, "job", relabel_tokens=True)
    ent._.trait = Job.from_ent(ent, job="collector", name=ent._.trait.name)
