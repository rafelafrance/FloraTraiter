from collections import namedtuple
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import regex as re
import traiter.pylib.darwin_core as t_dwc
from spacy.language import Language
from spacy.util import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import NS
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import ACCUMULATOR
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes import reject_match
from traiter.pylib.pipes import trait as t_trait
from traiter.pylib.traits import terms as t_terms
from traiter.pylib.traits.base import Base

Separated = namedtuple("Separated", "idx ent")


@dataclass(eq=False)
class Job(Base):
    # Class vars ----------
    job_terms: ClassVar[Path] = Path(__file__).parent / "terms" / "job_terms.csv"
    all_csvs: ClassVar[list[Path]] = [
        job_terms,
        Path(__file__).parent / "terms" / "id_num_terms.csv",
        Path(t_terms.__file__).parent / "name_terms.csv",
    ]

    replace: ClassVar[dict[str, str]] = {
        "".join(k.split()): v
        for k, v in term_util.term_data(job_terms, "replace").items()
    }

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

    temp: ClassVar[str] = "".join(
        t_const.OPEN + t_const.CLOSE + t_const.QUOTE + list(".,'&")
    )
    name_re: ClassVar[str] = re.compile(rf"^[\sa-z{re.escape(temp)}-]+$")
    # ---------------------

    job: str = None
    name: str | list[str] = None
    id_num: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        name = self.name if isinstance(self.name, str) else t_dwc.SEP.join(self.name)
        key = self.key
        kwargs = {key: name, self.key + "ID": self.id_num}
        if key.startswith(NS):
            return dwc.add(**kwargs)
        return dwc.add_dyn(**kwargs)

    @property
    def key(self) -> str:
        match self.job:
            case "collector" | "other_collector":
                key = DarwinCore.ns("recordedBy")
            case "determiner":
                key = DarwinCore.ns("identifiedBy")
            case _:
                key = self.key_builder(*self.job.split("_"))
        return key

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="job_terms", path=cls.all_csvs)

        job_overwrite = """name job_label num_label id_num""".split()
        add.trait_pipe(
            nlp,
            name="job_patterns",
            compiler=cls.job_patterns(),
            overwrite=job_overwrite,
            keep=[*ACCUMULATOR.keep, "not_name", "not_id_num"],
        )

        add.trait_pipe(
            nlp,
            name="other_patterns",
            compiler=cls.other_patterns(),
            overwrite=job_overwrite,
            keep=[*ACCUMULATOR.keep, "not_name", "not_id_num"],
        )

        add.custom_pipe(nlp, registered="separated_collector")

        add.trait_pipe(
            nlp,
            name="extend_job_names",
            compiler=cls.extend_job_name_patterns(),
            overwrite=["job"],
            keep=[*ACCUMULATOR.keep, "not_name", "not_id_num"],
        )

        add.custom_pipe(nlp, registered="name_only")

        add.trait_pipe(
            nlp,
            name="job_rename",
            compiler=cls.job_rename_patterns(),
            overwrite=["other_collector", "extend_job_names"],
        )

        delete = ["not_name", "name", "id_num", "job_label"]
        add.cleanup_pipe(nlp, name="person_cleanup", delete=delete)

    @classmethod
    def job_patterns(cls):
        return [
            Compiler(
                label="job",
                on_match="job_match",
                keep="job",
                decoder={
                    ":": {"LOWER": {"REGEX": rf"^(by|{cls.punct}+)$"}},
                    ",": {"LOWER": {"REGEX": rf"^({cls.punct}+)$"}},
                    "and": {"POS": {"IN": cls.conj}},
                    "bad": {"ENT_TYPE": {"IN": ["month"]}},
                    "by": {"LOWER": {"IN": ["by"]}},
                    "job_label": {"ENT_TYPE": "job_label"},
                    "id_num": {"ENT_TYPE": {"IN": ["id_num", "labeled_id_num"]}},
                    "maybe": {"POS": "PROPN"},
                    "name": {"ENT_TYPE": "name"},
                    "sep": {"LOWER": {"IN": cls.sep}},
                    "sp": {"IS_SPACE": True},
                },
                patterns=[
                    "job_label+ :* sp? name+",
                    "job_label+ :* sp? name+ sep sp? name+",
                    "job_label+ :* sp? name+ sep sp? name+ sep sp? name+",
                    "job_label+ :* sp? name+                           ,* sp? id_num+",
                    "job_label+ :* sp? name+ sep sp? name+             ,* sp? id_num+",
                    (
                        "job_label+ :* sp? name+ sep sp? name+ sep sp? name+ ,* sp? "
                        "id_num+"
                    ),
                    "                name+                             ,* sp? id_num+",
                    "                name+ sep sp? name+               ,* sp? id_num+",
                    "                name+ sep sp? name+ sep sp? name+ ,* sp? id_num+",
                    "id_num+        sp? name+",
                    "id_num+        sp? name+ sep sp? name+",
                    "id_num+        sp? name+ sep sp? name+ sep sp? name+",
                    "job_label+ :* sp? name+ sep sp? name+ sep sp? name+ sep sp? name+",
                    "job_label+ :* maybe? name+",
                    "job_label+ :* maybe? name+ and maybe? name+",
                ],
            ),
        ]

    @classmethod
    def other_patterns(cls):
        decoder = {
            "other_label": {"ENT_TYPE": "other_label"},
            "name": {"ENT_TYPE": "name"},
            "sep": {"LOWER": {"IN": cls.sep}},
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
                    (
                        "other_label+ sp? name+ sep* sp? name+ sep* sp? name+ sep* sp? "
                        "name+"
                    ),
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

    @classmethod
    def extend_job_name_patterns(cls):
        decoder = {
            "and": {"POS": {"IN": cls.conj}},
            "maybe": {"POS": "PROPN"},
            "name": {"ENT_TYPE": "name"},
            "other_collector": {"ENT_TYPE": "other_collector"},
            "sep": {"LOWER": {"IN": cls.sep}},
        }

        return [
            Compiler(
                label="extend_job_names",
                on_match="extend_job_names",
                decoder=decoder,
                patterns=[
                    " other_collector+ sep* name+ ",
                    " other_collector+ sep* maybe ",
                    " other_collector+ sep* name  and name+ ",
                    " other_collector+ sep* maybe and maybe maybe ",
                ],
            ),
        ]

    @classmethod
    def job_rename_patterns(cls):
        return Compiler(
            label="job",
            keep="job",
            on_match="job_rename_match",
            decoder={
                "rename": {"ENT_TYPE": {"IN": ["other_collector", "extend_job_names"]}},
            },
            patterns=[
                "rename+",
            ],
        )

    @classmethod
    def job_match(cls, ent):
        job = []
        people = []
        id_num = None

        for token in ent:
            if token._.flag == "skip" or token.ent_type_ == "num_label":
                continue

            elif token.ent_type_ == "job_label":
                job.append(token.lower_)

            elif token._.flag == "name":
                people.append(token._.trait.name)

            elif token._.flag == "id_num":
                id_num = token._.trait.id_num

            token._.flag = "skip"

        if not people:
            raise reject_match.RejectMatch

        job = "".join(job)
        job = cls.replace.get(job, job)
        job = job if job else "collector"

        name = people if len(people) > 1 else people[0]

        trait = cls.from_ent(ent, name=name, id_num=id_num, job=job)

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
    def extend_job_names(cls, ent):
        data = {}
        people = []

        for token in ent:
            if token._.flag == "other_collector":
                data = asdict(token._.trait)
                names = token._.trait.name
                people += names if isinstance(names, list) else [names]

            elif token._.flag == "skip" or token.text in cls.punct:
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


@registry.misc("job_match")
def job_match(ent):
    return Job.job_match(ent)


@registry.misc("other_match")
def other_match(ent):
    return Job.other_match(ent)


@registry.misc("extend_job_names")
def extend_job_names(ent):
    return Job.extend_job_names(ent)


@registry.misc("job_rename_match")
def job_rename_match(ent):
    return Job.job_rename_match(ent)


@Language.component("separated_collector")
def separated_collector(doc):
    """Look for collectors separated from their ID numbers."""
    name = None
    id_num = None

    for i, ent in enumerate(doc.ents):
        # Last name before an ID number
        if ent.label_ == "name" and not id_num:
            name = Separated(i, ent)

        # First ID number after a name
        elif ent.label_ == "id_num" and not id_num and name:
            id_num = Separated(i, ent)

    if name and id_num and id_num.idx - name.idx < 5:
        t_trait.relabel_entity(name.ent, "job", relabel_tokens=True)
        t_trait.relabel_entity(id_num.ent, "job", relabel_tokens=True)

        name_t = name.ent._.trait
        id_num_t = id_num.ent._.trait

        data = {"job": "collector", "name": name_t.name, "id_num": id_num_t.id_num}
        name.ent._.trait = Job.from_ent(name.ent, **data)
        id_num.ent._.trait = Job.from_ent(id_num.ent, **data)

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
