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

AND = ["and", "&"]
PUNCT = "[.:;,_-]"
SEP = ["and", "with", "et", *list("&._,;")]
CONJ = ["CCONJ", "ADP"]

NAME4 = [s for s in t_const.NAME_SHAPES if len(s) >= 4 and s[-1].isalpha()]
UPPER4 = [s for s in t_const.UPPER_SHAPES if len(s) >= 4 and s[-1].isalpha()]

NAME_RE = "".join(t_const.OPEN + t_const.CLOSE + t_const.QUOTE + list(".,'&"))
NAME_RE = re.compile(rf"^[\sa-z{re.escape(NAME_RE)}-]+$")


def build(nlp: Language, overwrite: Optional[list[str]] = None):
    add.term_pipe(nlp, name="person_terms", path=ALL_CSVS)

    overwrite = overwrite if overwrite else []

    add.trait_pipe(nlp, name="not_name_patterns", compiler=not_name_patterns())

    add.trait_pipe(
        nlp,
        name="name_patterns",
        compiler=name_patterns(),
        overwrite=overwrite + "name_prefix name_suffix no_label".split(),
        keep=[*ACCUMULATOR.keep, "job_label", "no_label", "not_name"],
    )

    job_overwrite = overwrite + """name job_label no_label id_no""".split()
    add.trait_pipe(
        nlp,
        name="job_patterns",
        compiler=job_patterns(),
        overwrite=job_overwrite,
    )

    add.custom_pipe(nlp, registered="separated_collector")

    add.trait_pipe(
        nlp,
        name="other_collector_patterns",
        compiler=other_collector_patterns(),
        overwrite=["job"],
        keep=[*ACCUMULATOR.keep, "not_name"],
    )

    add.custom_pipe(nlp, registered="name_only")

    add.cleanup_pipe(nlp, name="person_cleanup")


def not_name_patterns():
    decoder = {
        # "name": {"POS": {"IN": ["PROPN", "NOUN"]}},
        "name": {"SHAPE": {"IN": t_const.NAME_AND_UPPER}},
        "nope": {"ENT_TYPE": "not_name"},
    }

    return [
        Compiler(
            label="not_name",
            on_match=reject_match.REJECT_MATCH,
            decoder=decoder,
            patterns=[
                "      name+ nope+",
                "nope+ name+",
                "nope+ name+ nope+",
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
        "dr": {"ENT_TYPE": "name_prefix"},
        "id1": {"LOWER": {"REGEX": r"^(\w*\d+\w*)$"}},
        "id2": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
        "jr": {"ENT_TYPE": "name_suffix"},
        "name": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
        "name4": {"SHAPE": {"IN": NAME4}},
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
                "       name  -? name? -? pre? pre?   name4",
                "       name  -? name? -? pre? pre?   name4   _? jr+",
                "       name  -? name? -?   ambig",
                "       name  -? name? -?   ambig   _? jr+",
                "       ambig -? name? -? pre? pre?  name4 ",
                "       ambig -? name? -? pre? pre?  name4   _? jr+",
                "       A A? A?      pre? pre? name4",
                "       A A? A?      pre? pre? name4   _? jr+",
                "       name A A? A? pre? pre? name4",
                "       name A A? A? pre? pre? name4   _? jr+",
                "       name ..        name4",
                "       name ..        name4   _? jr+",
                "       name ( name )  name4",
                "       name ( name )  name4   _? jr+",
                "       name ( name )  name4",
                "dr+ _? name  -? name? -?  name4",
                "dr+ _? name  -? name? -?  name4   _? jr+",
                "dr+ _? name  -? name? -?  ambig",
                "dr+ _? name  -? name? -?  ambig   _? jr+",
                "dr+ _? ambig -? name? -?  name4",
                "dr+ _? ambig -? name? -?  name4   _? jr+",
                "dr+ _? A A? A?        name4",
                "dr+ _? A A? A?        name4   _? jr+",
                "dr+ _? name A A? A?   name4",
                "dr+ _? name A A? A?   name4   _? jr+",
                "dr+ _? name ..        name4",
                "dr+ _? name ..        name4   _? jr+",
                "dr+ _? name ( name )  name4",
                "dr+ _? name ( name )  name4   _? jr+",
                "dr+ _? name ( name )  name4",
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
                # " name_shape and name+ ",
                # " A A? A?    and name+ ",
                # "pre? pre? name4 , A? A? A",
                # "pre? pre? name4 ,? name",
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


def job_patterns():
    decoder = {
        ":": {"LOWER": {"REGEX": rf"^(by|{PUNCT}+)$"}},
        ",": {"LOWER": {"REGEX": rf"^({PUNCT}+)$"}},
        "and": {"POS": {"IN": CONJ}},
        "bad": {"ENT_TYPE": {"IN": ["month"]}},
        "by": {"LOWER": {"IN": ["by"]}},
        "det_label": {"ENT_TYPE": "det_label"},
        "job_label": {"ENT_TYPE": "job_label"},
        "id_no": {"ENT_TYPE": {"IN": ["id_no", "labeled_id_no"]}},
        "maybe": {"POS": "PROPN"},
        "name": {"ENT_TYPE": "name"},
        "nope": {"ENT_TYPE": "not_name"},
        "other_label": {"ENT_TYPE": "other_label"},
        "other_col": {"ENT_TYPE": "other_collector"},
        "sep": {"LOWER": {"IN": SEP}},
        "sp": {"IS_SPACE": True},
    }

    return [
        Compiler(
            label="job",
            on_match="job_match",
            keep="job",
            decoder=decoder,
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
                "job_label+ name+ ",
                "job_label+ name+ sep* sp? name+ ",
                "job_label+ name+ sep* sp? name+ sep* sp? name+ ",
                "job_label+ name+ sep* sp? name+ sep* sp? name+ sep* sp? name+ ",
                (
                    "job_label+ name+ sep* sp? name+ sep* sp? name+ sep* sp? "
                    "name+ sep* sp? name+"
                ),
                (
                    "job_label+ name+ sep* sp? name+ sep* sp? name+ sep* sp? "
                    "name+ sep* sp? name+ sep* sp? name+"
                ),
            ],
        ),
    ]


def other_collector_patterns():
    decoder = {
        "and": {"POS": {"IN": CONJ}},
        "maybe": {"POS": "PROPN"},
        "name": {"ENT_TYPE": "name"},
        "other_col": {"ENT_TYPE": "other_collector"},
        "sep": {"LOWER": {"IN": SEP}},
    }

    return [
        Compiler(
            label="extend_names",
            id="job",
            on_match="extend_names",
            keep="other_collector",
            decoder=decoder,
            patterns=[
                " other_col+ sep* name+ ",
                " other_col+ sep* maybe ",
                " other_col+ sep* name  and name+ ",
                " other_col+ sep* maybe and maybe maybe ",
            ],
        ),
    ]


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
            token._.flag = "name"

            # If there's a digit in the name reject it
            if re.search(r"\d", token.text):
                raise reject_match.RejectMatch

            # If it is all lower case reject it
            if token.text.islower() and token.ent_type_ != "last_prefix":
                raise reject_match.RejectMatch

        trait = cls.from_ent(ent, name=name)
        ent[0]._.trait = trait
        ent[0]._.flag = "name_data"
        return trait


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
            if token._.flag == "name" or token.ent_type_ == "no_label":
                continue

            elif token.ent_type_ == "job_label":
                job.append(token.lower_)

            elif token._.flag == "name_data":
                people.append(token._.trait.name)

            elif token._.flag == "id_no":
                id_no = token._.trait.id_no

            token._.flag = "skip"

        if not people or not job:
            raise reject_match.RejectMatch

        job = " ".join(job)
        job = job.replace(" :", ":")
        job = REPLACE.get(job, job)

        name = people if len(people) > 1 else people[0]

        trait = cls.from_ent(ent, name=name, id_no=id_no, job=job)

        ent[0]._.flag = job
        ent[0]._.trait = trait

        return trait

    @classmethod
    def extend_names(cls, ent):
        people = []
        person = []

        for token in ent:
            if token._.flag == "other_collector":
                people += token._.trait.name

            elif token._.flag == "skip" or token.text in PUNCT:
                continue

            else:
                person.append(token.text)

        if person:
            ent._.trait.name = [*people, " ".join(person)]


@registry.misc("name_match")
def name_match(ent):
    return Name.name_match(ent)


@registry.misc("id_no_match")
def id_no_match(ent):
    return IdNo.id_no_match(ent)


@registry.misc("job_match")
def job_match(ent):
    return Job.job_match(ent)


@registry.misc("extend_names")
def extend_names(ent):
    return Job.extend_names(ent)


@Language.component("separated_collector")
def separated_collector(doc):
    """Look for collectors separated from their ID numbers."""
    name = None
    collector = None
    dist = 0

    for ent in doc.ents:
        if dist:
            dist += 1
            if dist > 5:
                return doc

        if hasattr(ent._.trait, "job") and ent.trait.job == "collector":
            dist = 1
            collector = ent

        elif ent.label_ == "person" and not ent._.trait.job:
            dist = 1
            name = ent

        elif collector and ent.label_ == "labeled_id_no":
            collector_number(ent)

            collector._.trait.id_no = ent._.trait.id_no
            return doc

        elif name and ent.label_ == "labeled_id_no":
            collector_number(ent)

            t_trait.relabel_entity(name, "person")
            ent._.trait.name = name._.trait.name
            name._.trait.job = "collector"
            name._.trait.id_no = ent._.trait.id_no
            for token in name:
                token.ent_type_ = "person"
            return doc

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
    if not ent._.data.get("name"):
        return
    t_trait.relabel_entity(ent, "person")
    ent._.trait["job"] = "collector"
    for token in ent:
        token.ent_type_ = "person"


def collector_number(ent):
    t_trait.relabel_entity(ent, "person")
    for token in ent:
        token.ent_type_ = "person"
