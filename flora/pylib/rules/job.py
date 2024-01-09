from dataclasses import asdict, dataclass
from pathlib import Path
from typing import ClassVar

import regex as re
import traiter.pylib.darwin_core as t_dwc
from spacy.language import Language
from spacy.util import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.darwin_core import DWC, DarwinCore
from traiter.pylib.pattern_compiler import ACCUMULATOR, Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.rules import terms as t_terms
from traiter.pylib.rules.base import Base


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

    punct: ClassVar[list[str]] = "[.:;,_-]"
    and_: ClassVar[list[str]] = ["and", "with", "et"]
    sep: ClassVar[list[str]] = and_ + list("&._,;")
    conj: ClassVar[list[str]] = ["CCONJ", "ADP"]

    name4: ClassVar[list[str]] = [
        s for s in t_const.NAME_SHAPES if len(s) >= 4 and s[-1].isalpha()
    ]
    upper4: ClassVar[list[str]] = [
        s for s in t_const.UPPER_SHAPES if len(s) >= 4 and s[-1].isalpha()
    ]

    temp: ClassVar[str] = "".join(
        t_const.OPEN + t_const.CLOSE + t_const.QUOTE + list(".,'&"),
    )
    name_re: ClassVar[str] = re.compile(rf"^[\sa-z{re.escape(temp)}-]+$")
    # ---------------------

    job: str = None
    name: str | list[str] = None
    has_label: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        name = self.name if isinstance(self.name, str) else t_dwc.SEP.join(self.name)
        kwargs = {self.key: name}
        if self.key.startswith(DWC):
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

        add.trait_pipe(
            nlp,
            name="job_patterns",
            compiler=cls.job_patterns(),
            overwrite=["name", "job_label"],
            keep=[*ACCUMULATOR.keep, "not_name"],
        )
        # add.debug_tokens(nlp)  # ################################################

        add.trait_pipe(
            nlp,
            name="other_patterns",
            compiler=cls.other_patterns(),
            overwrite=["other_label", "job", "name"],
            keep=[*ACCUMULATOR.keep, "not_name"],
        )
        # add.debug_tokens(nlp)  # ################################################

        add.trait_pipe(
            nlp,
            name="extend_job_names",
            compiler=cls.extend_job_name_patterns(),
            overwrite=["job"],
            keep=[*ACCUMULATOR.keep, "not_name"],
        )
        # add.debug_tokens(nlp)  # ################################################

        add.trait_pipe(
            nlp,
            name="job_rename",
            compiler=cls.job_rename_patterns(),
            overwrite=["other_collector", "extend_job_names"],
        )
        # add.debug_tokens(nlp)  # ################################################

        delete = ["not_name", "name", "job_label", "other_label"]
        add.cleanup_pipe(nlp, name="person_cleanup", delete=delete)
        # add.debug_tokens(nlp)  # ################################################

    @classmethod
    def job_patterns(cls):
        return [
            Compiler(
                label="job",
                on_match="job_match",
                keep="job",
                decoder={
                    ",": {"LOWER": {"REGEX": rf"^({cls.punct}+)$"}},
                    ":": {"LOWER": {"REGEX": rf"^(by|{cls.punct}+)$"}},
                    "and": {"POS": {"IN": cls.conj}},
                    "bad": {"ENT_TYPE": {"IN": ["month"]}},
                    "by": {"LOWER": {"IN": ["by"]}},
                    "id_num": {"ENT_TYPE": "id_num"},
                    "job_label": {"ENT_TYPE": "job_label"},
                    "maybe": {"POS": "PROPN"},
                    "name": {"ENT_TYPE": "name"},
                    "sep": {"LOWER": {"IN": cls.sep}},
                    "sp": {"IS_SPACE": True},
                },
                patterns=[
                    "job_label+ :* maybe? name+ and maybe? name+",
                    "job_label+ :* maybe? name+",
                    "job_label+ :* sp? name+ sep sp? name+ ",
                    "job_label+ :* sp? name+ sep sp? name+ sep sp? name+ sep sp? name+",
                    "job_label+ :* sp? name+ sep sp? name+ sep sp? name+",
                    "job_label+ :* sp? name+ sep sp? name+",
                    "job_label+ :* sp? name+",
                    "maybe? name+ and maybe? name+",
                    "name+ sep sp? name+ ",
                    "name+ sep sp? name+ sep sp? name+ sep sp? name+",
                    "name+ sep sp? name+ sep sp? name+",
                    "name+ sep sp? name+",
                    "name+",
                ],
            ),
        ]

    @classmethod
    def other_patterns(cls):
        decoder = {
            "other_label": {"ENT_TYPE": "other_label"},
            "job": {"ENT_TYPE": "job"},
            "sep": {"LOWER": {"IN": cls.sep}},
            "sp": {"IS_SPACE": True},
        }

        return [
            Compiler(
                label="other_collector",
                on_match="other_match",
                decoder=decoder,
                patterns=[
                    "other_label+ sp? job+",
                    "other_label+ sp? job+ sep* sp? job+",
                    "other_label+ sp? job* sep* sp? job+ ",
                    "other_label+ sp? job* sp? job+ sep* sp? job+ ",
                    "other_label+ sp? job* sp? job+ sep* sp? job+ sep* sp? job+ ",
                    (
                        "other_label+ sp? job* sp? job+ sep* sp? job+ sep* sp? job+ "
                        "sep* sp? job+"
                    ),
                    (
                        "other_label+ sp? job* sp? job+ sep* sp? job+ sep* sp? job+ "
                        "sep* sp? job+ sep* sp? job+"
                    ),
                    (
                        "other_label+ sp? job* sp? job+ sep* sp? job+ sep* sp? job+ "
                        "sep* sp? job+ sep* sp? job+ sep* sp? job+"
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
        has_label = None

        for token in ent:
            if token._.flag == "skip" or token.ent_type_ == "num_label":
                continue

            elif token.ent_type_ == "job_label":
                has_label = True
                job.append(token.lower_)

            elif token._.flag == "name":
                people.append(token._.trait.name)

            token._.flag = "skip"

        if not people:
            raise reject_match.RejectMatch

        job = "".join(job)
        job = cls.replace.get(job, job)
        job = job if job else "collector"

        name = people if len(people) > 1 else people[0]

        trait = cls.from_ent(ent, name=name, job=job, has_label=has_label)

        ent[0]._.flag = "job"
        ent[0]._.trait = trait

        return trait

    @classmethod
    def other_match(cls, ent):
        people = []
        has_label = None

        for token in ent:
            if token._.flag == "job":
                name = token._.trait.name
                people += name if isinstance(name, list) else [name]

            elif token.ent_type_ == "other_label":
                has_label = True

            token._.flag = "skip"

        if not people:
            raise reject_match.RejectMatch

        name = people if len(people) > 1 else people[0]

        trait = cls.from_ent(ent, name=name, job="other_collector", has_label=has_label)

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
