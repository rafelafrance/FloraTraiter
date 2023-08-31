from pathlib import Path
from typing import Optional

import regex as re
from spacy.language import Language
from spacy.util import registry
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compiler import ACCUMULATOR
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes import reject_match
from traiter.pylib.pipes import trait
from traiter.pylib.traits import terms as t_terms

from flora.pylib.traits import terms as p_terms

PERSON_CSV = Path(__file__).parent / "terms" / "person_terms.csv"
NAME_CSV = Path(t_terms.__file__).parent / "name_terms.csv"
JOB_CSV = Path(p_terms.__file__).parent / "job_terms.csv"
ALL_CSVS = [PERSON_CSV, NAME_CSV, JOB_CSV]

PUNCT = "[.:;,_-]"
SEP = ["and", "with", "et", *list("&._,;")]

NAME4 = [s for s in t_const.NAME_SHAPES if len(s) >= 4 and s[-1].isalpha()]

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
        keep=[
            *ACCUMULATOR.keep,
            "col_label",
            "det_label",
            "job_label",
            "no_label",
            "not_name",
        ],
    )
    # add.debug_tokens(nlp)  # ##########################################

    job_overwrite = (
        overwrite
        + """
            name col_label det_label job_label no_label other_label id_no
            """.split()
    )
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
        overwrite=["other_collector"],
        keep=[*ACCUMULATOR.keep, "not_name"],
    )

    # add.debug_tokens(nlp)  # ##########################################
    add.custom_pipe(nlp, registered="name_only")

    add.cleanup_pipe(nlp, name="person_cleanup")


def not_name_patterns():
    decoder = {
        # "name": {"POS": {"IN": ["PROPN", "NOUN"]}},
        "name": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
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
        "-": {"TEXT": {"REGEX": r"^[._-]+$"}},
        ",": {"TEXT": {"IN": t_const.COMMA}},
        "..": {"TEXT": {"REGEX": r"^[.]+$"}},
        ":": {"LOWER": {"REGEX": rf"^(by|{PUNCT}+)$"}},
        "A": {"TEXT": {"REGEX": r"^[A-Z][._,]?$"}},
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
    }

    return [
        Compiler(
            label="name",
            on_match="person_name_match",
            decoder=decoder,
            patterns=[
                "       name  -? name? -?    name4",
                "       name  -? name? -?    name4   _? jr+",
                "       name  -? name? -?   ambig",
                "       name  -? name? -?   ambig   _? jr+",
                "       ambig -? name? -?   name4 ",
                "       ambig -? name? -?   name4   _? jr+",
                "       A A? A?        name4",
                "       A A? A?        name4   _? jr+",
                "       name A A? A?   name4",
                "       name A A? A?   name4   _? jr+",
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
            ],
        ),
        Compiler(
            label="id_no",
            on_match="id_no_match",
            decoder=decoder,
            patterns=[
                "no_space+ id1",
                "no_space+ id2",
                "id1",
            ],
        ),
        Compiler(
            label="labeled_id_no",
            on_match="id_no_match",
            decoder=decoder,
            patterns=[
                "no_label+ :* id1? no_space? id1? -? id2",
            ],
        ),
    ]


def job_patterns():
    decoder = {
        ":": {"LOWER": {"REGEX": rf"^(by|{PUNCT}+)$"}},
        "bad": {"ENT_TYPE": {"IN": ["month"]}},
        "by": {"LOWER": {"IN": ["by"]}},
        "col_label": {"ENT_TYPE": "col_label"},
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
            label="collector",
            on_match="collector_match",
            keep=["collector", "collector_no"],
            decoder=decoder,
            patterns=[
                "col_label+ :* name+",
                "col_label+ :* name+ sep sp? name+",
                "col_label+ :* name+ sep sp? name+ sep sp? name+",
                "col_label+ :* name+                             sp? id_no+",
                "col_label+ :* name+ sep sp? name+               sp? id_no+",
                "col_label+ :* name+ sep sp? name+ sep sp? name+ sp? id_no+",
                "              name+                             sp? id_no+",
                "              name+ sep sp? name+               sp? id_no+",
                "              name+ sep sp? name+ sep sp? name+ sp? id_no+",
                "id_no+        name+",
                "id_no+        name+ sep sp? name+",
                "id_no+        name+ sep sp? name+ sep sp? name+",
                "col_label+ :* name+ sep sp? name+ sep sp? name+ sep sp? name+",
            ],
        ),
        Compiler(
            label="other_collector",
            on_match="other_collector_match",
            keep="other_collector",
            decoder=decoder,
            patterns=[
                "other_label+ name+ ",
                "other_label+ name+ sep* sp? name+ ",
                "other_label+ name+ sep* sp? name+ sep* sp? name+ ",
                "other_label+ name+ sep* sp? name+ sep* sp? name+ sep* sp? name+ ",
                (
                    "other_label+ name+ sep* sp? name+ sep* sp? name+ sep* sp? "
                    "name+ sep* sp? name+"
                ),
                (
                    "other_label+ name+ sep* sp? name+ sep* sp? name+ sep* sp? "
                    "name+ sep* sp? name+ sep* sp? name+"
                ),
            ],
        ),
        Compiler(
            label="determiner",
            on_match="determiner_match",
            keep="determiner",
            decoder=decoder,
            patterns=[
                "det_label+ by? :* maybe? name+",
                "det_label+ by? :* name+ id_no+",
            ],
        ),
        Compiler(
            label="other_job",
            on_match="other_job_match",
            keep="other_job",
            decoder=decoder,
            patterns=[
                "job_label+ by? :* maybe? name+",
                "job_label+ by? :* name+ id_no+",
            ],
        ),
    ]


def other_collector_patterns():
    decoder = {
        "and": {"POS": {"IN": ["CCONJ", "ADP"]}},
        "maybe": {"POS": "PROPN"},
        "name": {"ENT_TYPE": "name"},
        "other_col": {"ENT_TYPE": "other_collector"},
        "sep": {"LOWER": {"IN": SEP}},
    }

    return [
        Compiler(
            label="other_collector2",
            id="other_collector",
            on_match="other_collector2_match",
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


@registry.misc("person_name_match")
def person_name_match(ent):
    name = ent.text
    name = re.sub(rf" ({PUNCT})", r"\1", name)
    name = re.sub(r"\.\.|_", "", name)

    if not NAME_RE.match(name.lower()):
        raise reject_match.RejectMatch

    for token in ent:
        token._.flag = "name"

        # Only accept proper nouns or nouns
        if len(token.text) > 1 and token.pos_ not in ("PROPN", "NOUN", "PUNCT", "AUX"):
            raise reject_match.RejectMatch

        # If there's a digit in the name reject it
        if re.search(r"\d", token.text):
            raise reject_match.RejectMatch

        # If it is all lower case reject it
        if token.text.islower():
            raise reject_match.RejectMatch

    ent._.data = {"name": name}
    ent[0]._.data = ent._.data
    ent[0]._.flag = "name_data"


@registry.misc("collector_match")
def collector_match(ent):
    people = []
    col_no = ""

    for token in ent:
        if token._.flag == "name_data":
            people.append(token._.data["name"])

        elif token._.flag == "name" or token.ent_type_ in ("col_label", "no_label"):
            continue

        elif token._.flag == "id_no":
            col_no = token._.data["id_no"]

    if not people:
        raise reject_match.RejectMatch

    ent._.data = {"collector": people if len(people) > 1 else people[0]}
    if col_no:
        ent._.data["collector_no"] = col_no


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

        if ent.label_ == "collector":
            dist = 1
            collector = ent

        elif ent.label_ == "name" and not collector:
            dist = 1
            name = ent

        elif collector and ent.label_ == "labeled_id_no":
            collector_number(ent)

            collector._.data["collector_no"] = ent._.data["collector_no"]
            return doc

        elif name and ent.label_ == "labeled_id_no":
            collector_number(ent)

            trait.relabel_entity(name, "collector")
            ent._.data["collector"] = name._.data["name"]
            name._.data["trait"] = "collector"
            name._.data["collector"] = name._.data["name"]
            name._.data["collector_no"] = ent._.data["collector_no"]
            del name._.data["name"]
            for token in name:
                token.ent_type_ = "collector"
            return doc

    return doc


def collector_number(ent):
    trait.relabel_entity(ent, "collector_no")
    ent._.data["trait"] = "collector_no"
    ent._.data["collector_no"] = ent._.data["id_no"]
    del ent._.data["id_no"]
    for token in ent:
        token.ent_type_ = "collector_no"


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
    trait.relabel_entity(ent, "collector")
    ent._.data["trait"] = "collector"
    ent._.data["collector"] = ent._.data["name"]
    del ent._.data["name"]
    for token in ent:
        token.ent_type_ = "collector"


@registry.misc("determiner_match")
def determiner_match(ent):
    people = []

    for token in ent:
        if token.ent_type_ == "det_label" or token.ent_type_ == "no_label":
            continue

        if token._.flag == "name_data":
            people.append(token._.data["name"])

        elif token._.flag == "id_no":
            ent._.data["determiner_no"] = token._.data["id_no"]

    ent._.data["determiner"] = " ".join(people)


@registry.misc("other_job_match")
def other_job_match(ent):
    people = []
    job = []

    for token in ent:
        if token.ent_type_ == "job_label":
            job.append(token.lower_)

        if token._.flag == "name_data":
            people.append(token._.data["name"])

        elif token._.flag == "id_no":
            ent._.data["id_no"] = token._.data["id_no"]

    ent._.data["job"] = " ".join(job)
    ent._.data["worker"] = " ".join(people)


@registry.misc("other_collector_match")
def other_collector_match(ent):
    people = []

    for token in ent:
        if token._.flag == "name_data":
            people.append(token._.data["name"])

        token._.flag = "other_col"

    ent._.data["other_collector"] = people
    ent[0]._.data = ent._.data
    ent[0]._.flag = "other_col_data"


@registry.misc("other_collector2_match")
def other_collector2_match(ent):
    people = []
    person = []

    for token in ent:
        if token._.flag == "other_col_data":
            people += token._.data["other_collector"]

        elif token._.flag == "other_col" or token.text in PUNCT:
            continue

        else:
            person.append(token.text)

    if person:
        ent._.data["other_collector"] = [*people, " ".join(person)]


@registry.misc("id_no_match")
def id_no_match(ent):
    frags = [t.text for t in ent if t.ent_type_ != "no_label"]
    frags = "".join(frags)
    frags = re.sub(r"^[,]", "", frags)
    ent._.data["id_no"] = frags
    ent[0]._.data = ent._.data
    ent[0]._.flag = "id_no"
