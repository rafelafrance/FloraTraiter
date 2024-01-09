import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.darwin_core as t_dwc
from spacy import Language, registry
from traiter.pylib import const as t_const
from traiter.pylib import taxon_util, term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import ACCUMULATOR, Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.rules import terms as t_terms
from traiter.pylib.rules.base import Base

from flora.pylib import const


def get_csvs() -> dict[str, Path]:
    here = Path(__file__).parent / "terms"
    csvs = {
        "name_terms": Path(t_terms.__file__).parent / "name_terms.csv",
        "taxon_terms": here / "taxon_terms.csv",
        "rank_terms": here / "rank_terms.csv",
        "binomial_terms": here / "binomial_terms.zip",
        "monomial_terms": here / "monomial_terms.zip",
    }

    try:
        use_mock_data = int(os.getenv("MOCK_DATA"))
    except (TypeError, ValueError):
        use_mock_data = 0

    if (
        not csvs["binomial_terms"].exists()
        or not csvs["monomial_terms"].exists()
        or use_mock_data
    ):
        csvs["binomial_terms"] = here / "mock_binomial_terms.csv"
        csvs["monomial_terms"] = here / "mock_monomial_terms.csv"

    return csvs


@dataclass(eq=False)
class Taxon(Base):
    # Class vars ----------
    all_csvs: ClassVar[dict[str, Path]] = get_csvs()

    rank_terms: ClassVar[list[dict]] = term_util.read_terms(all_csvs["rank_terms"])

    abbrev_re: ClassVar[str] = r"^[A-Z]?[.,_]?[A-Z][.,_]$"
    and_: ClassVar[list[str]] = ["&", "and", "et", "ex"]
    any_rank: ClassVar[list[str]] = sorted({r["label"] for r in rank_terms})
    auth3: ClassVar[list[str]] = [
        s for s in t_const.NAME_SHAPES if len(s) > 2 and s[-1] != "."
    ]
    auth3_upper: ClassVar[list[str]] = [
        s for s in t_const.NAME_AND_UPPER if len(s) > 2 and s[-1] != "."
    ]
    binomial_abbrev: ClassVar[dict[str, str]] = taxon_util.abbrev_binomial_term(
        all_csvs["binomial_terms"],
    )
    ambiguous: ClassVar[list[str]] = ["us_county", "color"]
    higher_rank: ClassVar[list[str]] = sorted(
        {r["label"] for r in rank_terms if r["level"] == "higher"},
    )
    level: ClassVar[dict[str, str]] = term_util.term_data(
        all_csvs["rank_terms"],
        "level",
    )
    linnaeus: ClassVar[list[str]] = "l l. lin lin. linn linn. linnaeus".split()
    lower_rank: ClassVar[list[str]] = sorted(
        {r["label"] for r in rank_terms if r["level"] == "lower"},
    )
    monomial_ranks: ClassVar[dict[str, str]] = term_util.term_data(
        all_csvs["monomial_terms"],
        "ranks",
    )
    rank_abbrev: ClassVar[dict[str, str]] = term_util.term_data(
        all_csvs["rank_terms"],
        "abbrev",
    )
    rank_replace: ClassVar[dict[str, str]] = term_util.term_data(
        all_csvs["rank_terms"],
        "replace",
    )
    # ---------------------

    taxon: str | list[str] = None
    rank: str = None
    authority: str | list[str] = None
    taxon_like: str = None
    associated: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        if self.level.get(self.rank) == "higher":
            return dwc.add(**{self.key: self.taxon})

        if self.associated:
            return dwc.add(associatedTaxa={"associated": self.taxon})

        auth = self.authority
        if isinstance(auth, list):
            auth = t_dwc.SEP.join(auth)

        return dwc.add(
            **{
                self.key: self._text,
                "taxonRank": self.rank,
                "scientificNameAuthorship": auth,
            },
        )

    @property
    def key(self) -> str:
        if self.level.get(self.rank) == "higher":
            return t_dwc.DarwinCore.ns(self.rank)

        return t_dwc.DarwinCore.ns(
            "associatedTaxa" if self.associated else "scientificName",
        )

    @classmethod
    def pipe(
        cls,
        nlp: Language,
        extend=1,
        overwrite: list[str] | None = None,
    ):
        overwrite = overwrite if overwrite else []

        default_labels = {
            "binomial_terms": "binomial",
            "monomial_terms": "monomial",
            "mock_binomial_terms": "binomial",
            "mock_monomial_terms": "monomial",
        }

        add.term_pipe(
            nlp,
            name="taxon_terms",
            path=list(cls.all_csvs.values()),
            default_labels=default_labels,
        )

        add.trait_pipe(
            nlp,
            name="taxon_patterns",
            compiler=cls.taxon_patterns(),
            merge=["taxon", "single"],
            overwrite=["taxon"],
        )

        add.trait_pipe(
            nlp,
            name="taxon_linnaeus_patterns",
            compiler=cls.taxon_linnaeus_patterns() + cls.multi_taxon_patterns(),
            merge=["linnaeus", "not_linnaeus"],
            overwrite=["taxon"],
        )

        # add.debug_tokens(nlp)  # ################################################
        auth_keep = [*ACCUMULATOR.keep, "single", "not_name"]
        add.trait_pipe(
            nlp,
            name="taxon_auth_patterns",
            compiler=cls.taxon_auth_patterns(),
            merge=["taxon"],
            keep=auth_keep,
            overwrite=["taxon", *overwrite],
        )
        # add.debug_tokens(nlp)  # ################################################

        for i in range(1, extend + 1):
            name = f"taxon_extend_{i}"
            add.trait_pipe(
                nlp,
                name=name,
                compiler=cls.taxon_extend_patterns(),
                merge=["taxon"],
                overwrite=["taxon", "linnaeus", "not_linnaeus", "single"],
            )

        add.trait_pipe(
            nlp,
            name="taxon_rename",
            compiler=cls.taxon_rename_patterns(),
            overwrite=["taxon", "linnaeus", "not_linnaeus", "single"],
        )

        add.cleanup_pipe(nlp, name="taxon_cleanup")

    @classmethod
    def taxon_patterns(cls):
        decoder = {
            ":": {"TEXT": {"IN": [":", ";"]}},
            "A.": {"TEXT": {"REGEX": cls.abbrev_re}},
            "bad_prefix": {"ENT_TYPE": "bad_taxon_prefix"},
            "bad_suffix": {"ENT_TYPE": "bad_taxon_suffix"},
            "maybe": {"POS": {"IN": ["PROPN", "NOUN"]}},
            "binomial": {"ENT_TYPE": "binomial"},
            "monomial": {"ENT_TYPE": "monomial"},
            "higher_rank": {"ENT_TYPE": {"IN": cls.higher_rank}},
            "subsp": {"ENT_TYPE": "subspecies_rank"},
            "var": {"ENT_TYPE": "variety_rank"},
            "subvar": {"ENT_TYPE": "subvariety_rank"},
            "f.": {"ENT_TYPE": "form_rank"},
            "subf": {"ENT_TYPE": "subform_rank"},
            "species_rank": {"ENT_TYPE": "species_rank"},
        }

        return [
            Compiler(
                label="single",
                on_match="single_taxon_match",
                decoder=decoder,
                patterns=[
                    "monomial",
                    "higher_rank  monomial",
                    "species_rank monomial",
                ],
            ),
            Compiler(
                label="species",
                id="taxon",
                keep="taxon",
                on_match="taxon_match",
                decoder=decoder,
                patterns=[
                    "binomial{2}",
                    "monomial monomial",
                    "A. monomial",
                ],
            ),
            Compiler(
                label="subspecies",
                id="taxon",
                keep="taxon",
                on_match="taxon_match",
                decoder=decoder,
                patterns=[
                    "   binomial{2} subsp? monomial",
                    "   binomial{2} subsp  maybe",
                    "A. monomial    subsp? monomial",
                    "A. monomial    subsp  maybe",
                    "A. maybe       subsp? monomial",
                    "A. maybe       subsp  maybe",
                ],
            ),
            Compiler(
                label="variety",
                id="taxon",
                keep="taxon",
                on_match="taxon_match",
                decoder=decoder,
                patterns=[
                    "   binomial{2}                var monomial",
                    "   binomial{2} subsp monomial var monomial",
                    "   binomial{2}                var maybe",
                    "   binomial{2} subsp monomial var maybe",
                    "A. monomial                   var monomial",
                    "A. monomial    subsp monomial var monomial",
                    "A. monomial                   var maybe",
                    "A. monomial    subsp monomial var maybe",
                    "A. monomial                   var monomial",
                    "A. monomial    subsp monomial var monomial",
                    "A. monomial                   var maybe",
                    "A. monomial    subsp monomial var maybe",
                    "A. maybe                      var monomial",
                    "A. maybe       subsp monomial var monomial",
                    "A. maybe                      var maybe",
                    "A. maybe       subsp monomial var maybe",
                    "A. maybe                      var monomial",
                    "A. maybe       subsp monomial var monomial",
                    "A. maybe                      var maybe",
                    "A. maybe       subsp monomial var maybe",
                ],
            ),
            Compiler(
                label="subvariety",
                id="taxon",
                keep="taxon",
                on_match="taxon_match",
                decoder=decoder,
                patterns=[
                    "   binomial{2}                subvar monomial",
                    "   binomial{2} var   monomial subvar monomial",
                    "   binomial{2} subsp monomial subvar monomial",
                    "   binomial{2}                subvar maybe",
                    "   binomial{2} var   monomial subvar maybe",
                    "   binomial{2} subsp monomial subvar maybe",
                    "   binomial{2} var   maybe    subvar maybe",
                    "   binomial{2} subsp maybe    subvar maybe",
                    "   binomial{2} var   maybe    subvar monomial",
                    "   binomial{2} subsp maybe    subvar monomial",
                    "A. monomial                   subvar monomial",
                    "A. monomial    var   monomial subvar monomial",
                    "A. monomial    subsp monomial subvar monomial",
                    "A. monomial                   subvar maybe",
                    "A. monomial    var   monomial subvar maybe",
                    "A. monomial    subsp monomial subvar maybe",
                    "A. monomial    var   maybe    subvar maybe",
                    "A. monomial    subsp maybe    subvar maybe",
                    "A. monomial    var   maybe    subvar monomial",
                    "A. monomial    subsp maybe    subvar monomial",
                    "A. maybe                      subvar monomial",
                    "A. maybe       var   monomial subvar monomial",
                    "A. maybe       subsp monomial subvar monomial",
                    "A. maybe                      subvar maybe",
                    "A. maybe       var   monomial subvar maybe",
                    "A. maybe       subsp monomial subvar maybe",
                    "A. maybe       var   maybe    subvar maybe",
                    "A. maybe       subsp maybe    subvar maybe",
                    "A. maybe       var   maybe    subvar monomial",
                    "A. maybe       subsp maybe    subvar monomial",
                ],
            ),
            Compiler(
                label="form",
                id="taxon",
                keep="taxon",
                on_match="taxon_match",
                decoder=decoder,
                patterns=[
                    "   binomial{2}                f. monomial",
                    "   binomial{2} var   monomial f. monomial",
                    "   binomial{2} subsp monomial f. monomial",
                    "   binomial{2}                f. maybe",
                    "   binomial{2} var   monomial f. maybe",
                    "   binomial{2} subsp monomial f. maybe",
                    "   binomial{2} var   maybe    f. maybe",
                    "   binomial{2} subsp maybe    f. maybe",
                    "   binomial{2} var   maybe    f. monomial",
                    "   binomial{2} subsp maybe    f. monomial",
                    "A. monomial                   f. monomial",
                    "A. monomial    var   monomial f. monomial",
                    "A. monomial    subsp monomial f. monomial",
                    "A. monomial                   f. maybe",
                    "A. monomial    var   monomial f. maybe",
                    "A. monomial    subsp monomial f. maybe",
                    "A. monomial    var   maybe    f. maybe",
                    "A. monomial    subsp maybe    f. maybe",
                    "A. monomial    var   maybe    f. monomial",
                    "A. monomial    subsp maybe    f. monomial",
                    "A. maybe                      f. monomial",
                    "A. maybe       var   monomial f. monomial",
                    "A. maybe       subsp monomial f. monomial",
                    "A. maybe                      f. maybe",
                    "A. maybe       var   monomial f. maybe",
                    "A. maybe       subsp monomial f. maybe",
                    "A. maybe       var   maybe    f. maybe",
                    "A. maybe       subsp maybe    f. maybe",
                    "A. maybe       var   maybe    f. monomial",
                    "A. maybe       subsp maybe    f. monomial",
                ],
            ),
            Compiler(
                label="subform",
                id="taxon",
                keep="taxon",
                on_match="taxon_match",
                decoder=decoder,
                patterns=[
                    "   binomial{2}                subf monomial",
                    "   binomial{2} var   monomial subf monomial",
                    "   binomial{2} subsp monomial subf monomial",
                    "   binomial{2}                subf maybe",
                    "   binomial{2} var   monomial subf maybe",
                    "   binomial{2} subsp monomial subf maybe",
                    "   binomial{2} var   maybe    subf maybe",
                    "   binomial{2} subsp maybe    subf maybe",
                    "   binomial{2} var   maybe    subf monomial",
                    "   binomial{2} subsp maybe    subf monomial",
                    "A. monomial                   subf monomial",
                    "A. monomial    var   monomial subf monomial",
                    "A. monomial    subsp monomial subf monomial",
                    "A. monomial                   subf maybe",
                    "A. monomial    var   monomial subf maybe",
                    "A. monomial    subsp monomial subf maybe",
                    "A. monomial    var   maybe    subf maybe",
                    "A. monomial    subsp maybe    subf maybe",
                    "A. monomial    var   maybe    subf monomial",
                    "A. monomial    subsp maybe    subf monomial",
                    "A. maybe                      subf monomial",
                    "A. maybe       var   monomial subf monomial",
                    "A. maybe       subsp monomial subf monomial",
                    "A. maybe                      subf maybe",
                    "A. maybe       var   monomial subf maybe",
                    "A. maybe       subsp monomial subf maybe",
                    "A. maybe       var   maybe    subf maybe",
                    "A. maybe       subsp maybe    subf maybe",
                    "A. maybe       var   maybe    subf monomial",
                    "A. maybe       subsp maybe    subf monomial",
                ],
            ),
            Compiler(
                label="bad_taxon",
                id="taxon",
                keep="taxon",
                decoder=decoder,
                on_match=reject_match.REJECT_MATCH,
                patterns=[
                    "bad_prefix :?    monomial",
                    "bad_prefix :? A. monomial",
                    "                 monomial    bad_suffix",
                    "              A. monomial    bad_suffix",
                    "bad_prefix :?    monomial    bad_suffix",
                    "bad_prefix :? A. monomial    bad_suffix",
                    "bad_prefix :?    binomial{2}",
                    "                 binomial{2} bad_suffix",
                    "bad_prefix :?    binomial{2} bad_suffix",
                ],
            ),
        ]

    @classmethod
    def multi_taxon_patterns(cls):
        return [
            Compiler(
                label="multi_taxon",
                keep="multi_taxon",
                on_match="multi_taxon_match",
                decoder={
                    "and": {"LOWER": {"IN": cls.and_}},
                    "taxon": {"ENT_TYPE": "taxon"},
                },
                patterns=[
                    "taxon and taxon",
                ],
            ),
        ]

    @classmethod
    def taxon_auth_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "A.": {"TEXT": {"REGEX": cls.abbrev_re}},
            "and": {"LOWER": {"IN": cls.and_}},
            "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
            "auth3": {"SHAPE": {"IN": cls.auth3}},
            "ambig": {"ENT_TYPE": {"IN": cls.ambiguous}},
            "by": {"LOWER": {"IN": ["by"]}},
            "linnaeus": {"ENT_TYPE": "linnaeus"},
            "taxon": {"ENT_TYPE": "taxon"},
            "_": {"TEXT": {"IN": list(":._;,")}},
            "id_num": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
        }

        return [
            Compiler(
                label="auth",
                id="taxon",
                on_match="taxon_auth_match",
                keep="taxon",
                decoder=decoder,
                patterns=[
                    "taxon ( ambig+ _? )",
                    "taxon ( A.* auth+ _? )",
                    "taxon ( A.* auth+ _? and  A.* auth+ _? )",
                    "taxon ( auth+  _? ) A.* auth* auth3 _?",
                    "taxon ( auth+  _? ) A.* auth* auth3 _? and A.* auth* auth3",
                    "taxon ( auth+ _? and  auth+ _?  ) A.* auth* auth3 _?",
                    "taxon by? A.* auth3 _?",
                    "taxon by? A.* auth  _?         auth3 _?",
                    "taxon by? A.* auth+ _? and A.* auth3 _?",
                    "taxon ( A.* auth+   _? and A.* auth+ _? and A.* auth+ _? )",
                    (
                        "taxon ( A.* auth+  _? and A.* auth+ _? and A.* auth+ _? ) "
                        "A.* auth* auth3 _?"
                    ),
                    (
                        "taxon ( A.* auth+  _? and A.* auth+ _? and A.* auth+ _? ) "
                        "A.* auth* auth3 _? and A.* auth* auth3 _?"
                    ),
                ],
            ),
            Compiler(
                label="not_auth",
                id="taxon",
                on_match=reject_match.REJECT_MATCH,
                decoder=decoder,
                patterns=[
                    "taxon auth      id_num",
                    "taxon auth auth id_num",
                ],
            ),
        ]

    @classmethod
    def taxon_linnaeus_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            ".": {"TEXT": {"IN": t_const.DOT}},
            "_": {"TEXT": {"IN": list(":._;,")}},
            "A.": {"TEXT": {"REGEX": cls.abbrev_re}},
            "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
            "auth3": {"SHAPE": {"IN": cls.auth3}},
            "L.": {"TEXT": {"REGEX": r"^L[.,_]$"}},
            "linnaeus": {"LOWER": {"IN": cls.linnaeus}},
            "taxon": {"ENT_TYPE": "taxon"},
        }

        return [
            Compiler(
                label="linnaeus",
                on_match="taxon_linnaeus_match",
                decoder=decoder,
                patterns=[
                    "taxon ( linnaeus )",
                    "taxon   linnaeus ",
                    "taxon ( linnaeus ) A.+  auth3 _?",
                    "taxon ( linnaeus )      auth3 _?",
                    "taxon ( linnaeus ) auth auth3 _?",
                ],
            ),
            Compiler(
                label="not_linnaeus",
                on_match="taxon_not_linnaeus_match",
                decoder=decoder,
                patterns=[
                    "taxon L. .? auth3",
                ],
            ),
        ]

    @classmethod
    def taxon_extend_patterns(cls):
        return [
            Compiler(
                label="extend",
                id="taxon",
                keep="taxon",
                on_match="taxon_extend_match",
                decoder={
                    "(": {"TEXT": {"IN": t_const.OPEN}},
                    ")": {"TEXT": {"IN": t_const.CLOSE}},
                    "_": {"TEXT": {"IN": list(":._;,")}},
                    "A.": {"TEXT": {"REGEX": cls.abbrev_re}},
                    "ambig": {"ENT_TYPE": {"IN": cls.ambiguous}},
                    "and": {"LOWER": {"IN": cls.and_}},
                    "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
                    "auth3": {"SHAPE": {"IN": cls.auth3}},
                    "by": {"LOWER": {"IN": ["by"]}},
                    "single": {"ENT_TYPE": "single"},
                    "sp": {"IS_SPACE": True},
                    "taxon": {
                        "ENT_TYPE": {"IN": ["taxon", "linnaeus", "not_linnaeus"]},
                    },
                    "l_rank": {"ENT_TYPE": {"IN": cls.lower_rank}},
                },
                patterns=[
                    "taxon sp? l_rank+ single",
                    "taxon sp? l_rank+ single ( auth+ _? ) ",
                    "taxon sp? l_rank+ single ( auth+ _? and auth+ _? ) ",
                    "taxon sp? l_rank+ single by? auth* auth3 _? ",
                    "taxon sp? l_rank+ single by? auth+ auth3 _? and auth* auth3 _? ",
                    "taxon sp? l_rank+ single by? A.* auth3 _?          ",
                    "taxon sp? l_rank+ single by? A.* auth+ _? auth3 _? ",
                    "taxon sp? l_rank+ single by? A.* auth+ _? and A.* auth3 _? ",
                    "taxon sp? l_rank+ single ( auth+  _? ) A.+  auth3 _?",
                    "taxon sp? l_rank+ single ( auth+  _? )      auth3 _?",
                    "taxon sp? l_rank+ single ( auth+  _? ) auth3 _? and auth* auth3 _? ",
                    "taxon sp? l_rank+ single ( ambig+ _? ) auth3 _?",
                    "taxon sp? l_rank+ single ( auth+ _? and  auth+ _? ) auth auth3 _?",
                    "taxon sp? l_rank+ single ( auth+ _? and  auth+ _? ) A.+  auth3 _?",
                ],
            ),
        ]

    @classmethod
    def taxon_rename_patterns(cls):
        return Compiler(
            label="taxon",
            keep="taxon",
            on_match="rename_taxon_match",
            decoder={
                "taxon": {"ENT_TYPE": {"IN": ["single", "linnaeus", "not_linnaeus"]}},
                "rank": {"ENT_TYPE": {"IN": cls.any_rank}},
            },
            patterns=[
                "taxon",
                "rank taxon",
            ],
        )

    @classmethod
    def taxon_match(cls, ent):
        taxon = []
        rank_seen = False

        for i, token in enumerate(ent):
            token._.flag = "taxon"

            if cls.level.get(token.lower_) == "lower":
                taxon.append(cls.rank_abbrev.get(token.lower_, token.lower_))
                rank_seen = True

            elif token._.term == "binomial" and i == 0:
                taxon.append(token.text.title())

            elif token._.term == "binomial" and i > 0:
                taxon.append(token.lower_)

            elif token._.term == "monomial" and i != 2:
                taxon.append(token.lower_)

            elif token._.term == "monomial" and i == 2:
                if not rank_seen:
                    taxon.append(cls.rank_abbrev["subspecies"])
                taxon.append(token.lower_)

            elif token.pos_ in ["PROPN", "NOUN"]:
                taxon.append(token.text)

            else:
                raise reject_match.RejectMatch

        if re.match(cls.abbrev_re, taxon[0]) and len(taxon) > 1:
            taxon[0] = taxon[0] if taxon[0][-1] == "." else taxon[0] + "."
            abbrev = " ".join(taxon[:2])
            taxon[0] = cls.binomial_abbrev.get(abbrev, taxon[0])

        taxon = " ".join(taxon)
        taxon = taxon[0].upper() + taxon[1:]

        trait = cls.from_ent(ent, taxon=taxon, rank=ent.label_)

        ent[0]._.trait = trait
        ent[0]._.flag = "taxon_data"

        return trait

    @classmethod
    def single_taxon_match(cls, ent):
        rank = None
        taxon = None

        for token in ent:
            token._.flag = "taxon"

            # Taxon and its rank
            if token._.term == "monomial":
                taxon = token.lower_
                taxon = taxon.replace("- ", "-")

                # A given rank will override the one in the DB
                rank_ = cls.monomial_ranks.get(token.lower_)
                if not rank and rank_:
                    rank_ = rank_.split()[0]
                    level = cls.level[rank_]
                    if level == "higher" and token.shape_ in t_const.NAME_AND_UPPER:
                        rank = rank_
                    elif (
                        level in ("lower", "species")
                        and token.shape_ not in t_const.TITLE_SHAPES
                    ):
                        rank = rank_

            # A given rank overrides the one in the DB
            elif cls.level.get(token.lower_) in ("higher", "lower"):
                rank = cls.rank_replace.get(token.lower_, token.lower_)

            elif token.pos_ in ("PROPN", "NOUN"):
                taxon = token.lower_

        if not rank:
            raise reject_match.RejectMatch

        taxon = taxon.title() if cls.level[rank] == "higher" else taxon.lower()

        if len(taxon) < const.MIN_TAXON_LEN:
            raise reject_match.RejectMatch

        trait = cls.from_ent(ent, taxon=taxon, rank=rank)

        ent[0]._.trait = trait
        ent[0]._.flag = "taxon_data"

        return trait

    @classmethod
    def multi_taxon_match(cls, ent):
        taxa = []
        rank = None

        for sub_ent in ent.ents:
            taxa.append(sub_ent._.trait.taxon)
            rank = sub_ent._.trait.rank

        return cls.from_ent(ent, taxon=taxa, rank=rank)

    @classmethod
    def taxon_auth_match(cls, ent):
        auth = []
        prev_auth = None
        data = {}

        for token in ent:
            if token._.flag == "taxon_data":
                data = asdict(token._.trait)
                if token._.trait.authority:
                    prev_auth = token._.trait.authority

            elif auth and token.lower_ in cls.and_:
                auth.append("and")

            elif token.shape_ in t_const.NAME_SHAPES or re.match(
                cls.abbrev_re,
                token.text,
            ):
                if len(token) == 1:
                    auth.append(token.text + ".")
                else:
                    auth.append(token.text)

            token._.flag = "taxon"

        auth = " ".join(auth)
        data["authority"] = [prev_auth, auth] if prev_auth else auth

        trait = cls.from_ent(ent, **data)

        ent[0]._.trait = trait
        ent[0]._.flag = "taxon_data"

        return trait

    @classmethod
    def taxon_linnaeus_match(cls, ent):
        auth = []
        data = {}
        for token in ent:
            if token._.flag == "taxon_data":
                data = asdict(token._.trait)
            elif token.lower_ in cls.linnaeus:
                pass
            elif token.shape_ in t_const.NAME_SHAPES:
                if len(token) == 1:
                    auth.append(token.text + ".")
                else:
                    auth.append(token.text)

        data["authority"] = ", ".join(["Linnaeus", *auth])
        trait = cls.from_ent(ent, **data)

        ent[0]._.trait = trait
        ent[0]._.flag = "taxon_data"

        return trait

    @classmethod
    def taxon_not_linnaeus_match(cls, ent):
        auth = []
        data = {}
        for token in ent:
            if token._.flag == "taxon_data":
                data = asdict(token._.trait)

            elif token.shape_ in t_const.NAME_SHAPES:
                if len(token) == 1:
                    auth.append(token.text + ".")
                else:
                    auth.append(token.text)

            token._.flag = "taxon"

        data["authority"] = " ".join(auth)
        trait = cls.from_ent(ent, **data)

        ent[0]._.trait = trait
        ent[0]._.flag = "taxon_data"

        return trait

    @classmethod
    def taxon_extend_match(cls, ent):
        auth = []
        taxon = []
        rank = ""
        next_is_lower_taxon = False

        for token in ent:
            if token._.flag == "taxon_data":
                taxon.append(token._.trait.taxon)
                if token._.trait.authority:
                    auth.append(token._.trait.authority)

            elif token._.flag == "taxon" or token.text in "().":
                pass

            elif auth and token.lower_ in cls.and_:
                pass

            elif token.shape_ in t_const.NAME_SHAPES:
                if len(token) == 1:
                    auth.append(token.text + ".")
                else:
                    auth.append(token.text)

            elif token._.term in cls.lower_rank:
                taxon.append(cls.rank_abbrev.get(token.lower_, token.lower_))
                rank = cls.rank_replace.get(token.lower_, token.text)
                next_is_lower_taxon = True

            elif next_is_lower_taxon:
                taxon.append(token.lower_)
                next_is_lower_taxon = False

            token._.flag = "taxon"

        trait = cls.from_ent(ent, authority=auth, rank=rank, taxon=" ".join(taxon))

        ent._.relabel = "taxon"

        ent[0]._.trait = trait
        ent[0]._.flag = "taxon_data"

        return trait

    @classmethod
    def rename_taxon_match(cls, ent):
        rank = ""
        data = {}

        for token in ent:
            if token._.flag == "taxon_data":
                data = asdict(token._.trait)

            elif token._.term in cls.any_rank:
                rank = cls.rank_replace.get(token.lower_, token.lower_)

        ent._.relabel = "taxon"

        trait = cls.from_ent(ent, **data)

        if rank:
            trait.rank = rank

        ent[0]._.trait = trait
        ent[0]._.flag = "taxon_data"

        return trait


@registry.misc("taxon_match")
def taxon_match(ent):
    return Taxon.taxon_match(ent)


@registry.misc("single_taxon_match")
def single_taxon_match(ent):
    return Taxon.single_taxon_match(ent)


@registry.misc("multi_taxon_match")
def multi_taxon_match(ent):
    return Taxon.multi_taxon_match(ent)


@registry.misc("taxon_auth_match")
def taxon_auth_match(ent):
    return Taxon.taxon_auth_match(ent)


@registry.misc("taxon_linnaeus_match")
def taxon_linnaeus_match(ent):
    return Taxon.taxon_linnaeus_match(ent)


@registry.misc("taxon_not_linnaeus_match")
def taxon_not_linnaeus_match(ent):
    return Taxon.taxon_not_linnaeus_match(ent)


@registry.misc("taxon_extend_match")
def taxon_extend_match(ent):
    return Taxon.taxon_extend_match(ent)


@registry.misc("rename_taxon_match")
def rename_taxon_match(ent):
    return Taxon.rename_taxon_match(ent)
