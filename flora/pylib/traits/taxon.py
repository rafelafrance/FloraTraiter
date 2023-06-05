import os
import re
from pathlib import Path

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import taxon_util
from traiter.pylib import term_util
from traiter.pylib.traits import terms as t_terms
from traiter.pylib.pattern_compiler import ACCUMULATOR
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.pipes import reject_match

from .. import const


def get_csvs():
    here = Path(__file__).parent / "terms"
    csvs = {
        "name_terms": Path(t_terms.__file__).parent / "name_terms.csv",
        "taxon_terms": here / "taxon_terms.csv",
        "rank_terms": here / "rank_terms.csv",
        "binomial_terms": here / "binomial_terms.zip",
        "monomial_terms": here / "monomial_terms.zip",
    }

    try:
        use_mock_taxa = int(os.getenv("MOCK_TAXA"))
    except (TypeError, ValueError):
        use_mock_taxa = 0

    if (
        not csvs["binomial_terms"].exists()
        or not csvs["monomial_terms"].exists()
        or use_mock_taxa
    ):
        csvs["binomial_terms"] = here / "mock_binomial_terms.csv"
        csvs["monomial_terms"] = here / "mock_monomial_terms.csv"

    return csvs


ALL_CSVS = get_csvs()

RANK_TERMS = term_util.read_terms(ALL_CSVS["rank_terms"])

ABBREV_RE = r"^[A-Z][.,_]$"
AND = ["&", "and", "et"]
ANY_RANK = sorted({r["label"] for r in RANK_TERMS})
AUTH3 = [s for s in t_const.NAME_SHAPES if len(s) > 2 and s[-1] != "."]
AUTH3_UPPER = [s for s in t_const.NAME_AND_UPPER if len(s) > 2 and s[-1] != "."]
BINOMIAL_ABBREV = taxon_util.abbrev_binomial_term(ALL_CSVS["binomial_terms"])
AMBIGUOUS = ["us_county", "color"]
HIGHER_RANK = sorted({r["label"] for r in RANK_TERMS if r["level"] == "higher"})
LEVEL = term_util.term_data(ALL_CSVS["rank_terms"], "level")
LINNAEUS = ["l", "l.", "lin", "lin.", "linn", "linn.", "linnaeus"]
LOWER_RANK = sorted({r["label"] for r in RANK_TERMS if r["level"] == "lower"})
MONOMIAL_RANKS = term_util.term_data(ALL_CSVS["monomial_terms"], "ranks")
RANK_ABBREV = term_util.term_data(ALL_CSVS["rank_terms"], "abbrev")
RANK_REPLACE = term_util.term_data(ALL_CSVS["rank_terms"], "replace")


def build(
    nlp: Language, extend=1, overwrite: list[str] = None, auth_keep: list[str] = None
):
    overwrite = overwrite if overwrite else []
    auth_keep = auth_keep if auth_keep else []

    default_labels = {
        "binomial_terms": "binomial",
        "monomial_terms": "monomial",
        "mock_binomial_terms": "binomial",
        "mock_monomial_terms": "monomial",
    }

    add.term_pipe(
        nlp,
        name="taxon_terms",
        path=list(ALL_CSVS.values()),
        default_labels=default_labels,
    )

    add.trait_pipe(
        nlp,
        name="taxon_patterns",
        compiler=taxon_patterns(),
        merge=["taxon", "singleton"],
        overwrite=["taxon"],
    )
    # add.debug_tokens(nlp)  # ###############################

    add.trait_pipe(
        nlp,
        name="taxon_linnaeus_patterns",
        compiler=taxon_linnaeus_patterns() + multi_taxon_patterns(),
        merge=["linnaeus", "not_linnaeus"],
        overwrite=["taxon"],
    )
    # add.debug_tokens(nlp)  # ###############################

    auth_keep = auth_keep + ACCUMULATOR.keep + ["singleton", "not_name"]
    add.trait_pipe(
        nlp,
        name="taxon_auth_patterns",
        compiler=taxon_auth_patterns(),
        merge=["taxon"],
        keep=auth_keep,
        overwrite=["taxon", *overwrite],
    )

    # add.debug_tokens(nlp)  # ###############################
    for i in range(1, extend + 1):
        name = f"taxon_extend_{i}"
        add.trait_pipe(
            nlp,
            name=name,
            compiler=taxon_extend_patterns(),
            merge=["taxon"],
            overwrite=["taxon", "linnaeus", "not_linnaeus", "singleton"],
        )

    add.trait_pipe(
        nlp,
        name="taxon_rename",
        compiler=taxon_rename_patterns(),
        overwrite=["taxon", "linnaeus", "not_linnaeus", "singleton"],
    )

    add.cleanup_pipe(nlp, name="taxon_cleanup")


def taxon_patterns():
    decoder = {
        ":": {"TEXT": {"IN": [":", ";"]}},
        "A.": {"TEXT": {"REGEX": ABBREV_RE}},
        "bad_prefix": {"ENT_TYPE": "bad_taxon_prefix"},
        "bad_suffix": {"ENT_TYPE": "bad_taxon_suffix"},
        "maybe": {"POS": {"IN": ["PROPN", "NOUN"]}},
        "binomial": {"ENT_TYPE": "binomial"},
        "monomial": {"ENT_TYPE": "monomial"},
        "higher_rank": {"ENT_TYPE": {"IN": HIGHER_RANK}},
        "subsp": {"ENT_TYPE": "subspecies_rank"},
        "var": {"ENT_TYPE": "variety_rank"},
        "subvar": {"ENT_TYPE": "subvariety_rank"},
        "f.": {"ENT_TYPE": "form_rank"},
        "subf": {"ENT_TYPE": "subform_rank"},
        "species_rank": {"ENT_TYPE": "species_rank"},
    }

    return [
        Compiler(
            label="singleton",
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


def multi_taxon_patterns():
    return [
        Compiler(
            label="multi_taxon",
            keep="multi_taxon",
            on_match="multi_taxon_match",
            decoder={
                "and": {"LOWER": {"IN": AND}},
                "taxon": {"ENT_TYPE": "taxon"},
            },
            patterns=[
                "taxon and taxon",
            ],
        )
    ]


def taxon_auth_patterns():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        "and": {"LOWER": {"IN": AND}},
        "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
        "auth3": {"SHAPE": {"IN": AUTH3}},
        "ambig": {"ENT_TYPE": {"IN": AMBIGUOUS}},
        "linnaeus": {"ENT_TYPE": "linnaeus"},
        "taxon": {"ENT_TYPE": "taxon"},
        "_": {"TEXT": {"IN": list(":._;,")}},
        "id_no": {"LOWER": {"REGEX": r"^(\w*\d+\w*|[A-Za-z])$"}},
    }

    return [
        Compiler(
            label="auth",
            id="taxon",
            on_match="taxon_auth_match",
            keep="taxon",
            decoder=decoder,
            patterns=[
                "taxon ( auth+             _? )",
                "taxon ( ambig+            _? )",
                "taxon ( auth+ and   auth+ _? )",
                "taxon ( auth+             _? )      auth3",
                "taxon ( ambig+            _? )      auth3",
                "taxon ( auth+ and   auth+ _? ) auth auth3",
                "taxon   auth3",
                "taxon   auth        auth3",
                "taxon   auth+ and   auth3",
            ],
        ),
        Compiler(
            label="not_auth",
            id="taxon",
            on_match=reject_match.REJECT_MATCH,
            decoder=decoder,
            patterns=[
                "taxon auth      id_no",
                "taxon auth auth id_no",
            ],
        ),
    ]


def taxon_linnaeus_patterns():
    decoder = {
        "(": {"TEXT": {"IN": t_const.OPEN}},
        ")": {"TEXT": {"IN": t_const.CLOSE}},
        ".": {"TEXT": {"IN": t_const.DOT}},
        "auth3": {"SHAPE": {"IN": AUTH3}},
        "L.": {"TEXT": {"REGEX": r"^L[.,_]$"}},
        "linnaeus": {"LOWER": {"IN": LINNAEUS}},
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


def taxon_extend_patterns():
    return [
        Compiler(
            label="extend",
            id="taxon",
            keep="taxon",
            on_match="taxon_extend_match",
            decoder={
                "(": {"TEXT": {"IN": t_const.OPEN}},
                ")": {"TEXT": {"IN": t_const.CLOSE}},
                "and": {"LOWER": {"IN": AND}},
                "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
                "auth3": {"SHAPE": {"IN": AUTH3}},
                "singleton": {"ENT_TYPE": "singleton"},
                "taxon": {"ENT_TYPE": {"IN": ["taxon", "linnaeus", "not_linnaeus"]}},
                "lower_rank": {"ENT_TYPE": {"IN": LOWER_RANK}},
            },
            patterns=[
                "taxon lower_rank+ singleton",
                "taxon lower_rank+ singleton ( auth+           )",
                "taxon lower_rank+ singleton ( auth+ and auth+ )",
                "taxon lower_rank+ singleton ( auth+ and auth+ )",
                "taxon lower_rank+ singleton   auth3            ",
                "taxon lower_rank+ singleton   auth+ auth3      ",
                "taxon lower_rank+ singleton   auth+ and auth3  ",
            ],
        ),
    ]


def taxon_rename_patterns():
    return Compiler(
        label="taxon",
        keep="taxon",
        on_match="rename_taxon_match",
        decoder={
            "taxon": {"ENT_TYPE": {"IN": ["singleton", "linnaeus", "not_linnaeus"]}},
            "rank": {"ENT_TYPE": {"IN": ANY_RANK}},
        },
        patterns=[
            "taxon",
            "rank taxon",
        ],
    )


@registry.misc("taxon_match")
def taxon_match(ent):
    taxon = []
    rank_seen = False

    for i, token in enumerate(ent):
        token._.flag = "taxon"

        if LEVEL.get(token.lower_) == "lower":
            taxon.append(RANK_ABBREV.get(token.lower_, token.lower_))
            rank_seen = True

        elif token._.term == "binomial" and i == 0:
            taxon.append(token.text.title())

        elif token._.term == "binomial" and i > 0:
            taxon.append(token.lower_)

        elif token._.term == "monomial" and i != 2:
            taxon.append(token.lower_)

        elif token._.term == "monomial" and i == 2:
            if not rank_seen:
                taxon.append(RANK_ABBREV["subspecies"])
            taxon.append(token.lower_)

        elif token.pos_ in ["PROPN", "NOUN"]:
            taxon.append(token.text)

        else:
            raise reject_match.RejectMatch()

    if re.match(ABBREV_RE, taxon[0]) and len(taxon) > 1:
        taxon[0] = taxon[0] if taxon[0][-1] == "." else taxon[0] + "."
        abbrev = " ".join(taxon[:2])
        taxon[0] = BINOMIAL_ABBREV.get(abbrev, taxon[0])

    taxon = " ".join(taxon)
    taxon = taxon[0].upper() + taxon[1:]

    ent._.data = {"taxon": taxon, "rank": ent.label_}
    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc("single_taxon_match")
def single_taxon_match(ent):
    rank = None
    taxon = None

    for token in ent:
        token._.flag = "taxon"

        # Taxon and its rank
        if token._.term == "monomial":
            taxon = token.lower_
            taxon = taxon.replace("- ", "-")

            # A given rank will override the one in the DB
            rank_ = MONOMIAL_RANKS.get(token.lower_)
            if not rank and rank_:
                rank_ = rank_.split()[0]
                level = LEVEL[rank_]
                if level == "higher" and token.shape_ in t_const.NAME_AND_UPPER:
                    rank = rank_
                elif (
                    level in ("lower", "species")
                    and token.shape_ not in t_const.TITLE_SHAPES
                ):
                    rank = rank_

        # A given rank overrides the one in the DB
        elif LEVEL.get(token.lower_) in ("higher", "lower"):
            rank = RANK_REPLACE.get(token.lower_, token.lower_)

        elif token.pos_ in ("PROPN", "NOUN"):
            taxon = token.lower_

    if not rank:
        raise reject_match.RejectMatch

    taxon = taxon.title() if LEVEL[rank] == "higher" else taxon.lower()
    if len(taxon) < const.MIN_TAXON_LEN:
        raise reject_match.RejectMatch

    ent._.data = {
        "taxon": taxon.title() if LEVEL[rank] == "higher" else taxon.lower(),
        "rank": rank,
    }
    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc("multi_taxon_match")
def multi_taxon_match(ent):
    taxa = []

    for sub_ent in ent.ents:
        taxa.append(sub_ent._.data["taxon"])
        ent._.data["rank"] = sub_ent._.data["rank"]

    ent._.data["taxon"] = taxa


@registry.misc("taxon_auth_match")
def taxon_auth_match(ent):
    auth = []
    prev_auth = None
    data = {}

    for token in ent:

        if token._.flag == "taxon_data":
            data = token._.data
            prev_auth = token._.data.get("authority")

        elif auth and token.lower_ in AND:
            auth.append("and")

        elif token.shape_ in t_const.NAME_SHAPES:
            if len(token) == 1:
                auth.append(token.text + ".")
            else:
                auth.append(token.text)

        token._.flag = "taxon"

    ent._.data = data

    auth = " ".join(auth)
    ent._.data["authority"] = [prev_auth, auth] if prev_auth else auth

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc("taxon_linnaeus_match")
def taxon_linnaeus_match(ent):
    for token in ent:

        if token._.flag == "taxon_data":
            ent._.data = token._.data

    ent._.data["authority"] = "Linnaeus"

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc("taxon_not_linnaeus_match")
def taxon_not_linnaeus_match(ent):
    auth = []
    for token in ent:

        if token._.flag == "taxon_data":
            ent._.data = token._.data

        elif token.shape_ in t_const.NAME_SHAPES:
            if len(token) == 1:
                auth.append(token.text + ".")
            else:
                auth.append(token.text)

        token._.flag = "taxon"

    ent._.data["authority"] = " ".join(auth)

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc("taxon_extend_match")
def taxon_extend_match(ent):
    auth = []
    taxon = []
    rank = ""
    next_is_lower_taxon = False

    for token in ent:
        if token._.flag == "taxon_data":
            ent._.data = token._.data
            taxon.append(ent._.data["taxon"])
            if ent._.data.get("authority"):
                auth.append(ent._.data["authority"])

        elif token._.flag == "taxon" or token.text in "().":
            pass

        elif auth and token.lower_ in AND:
            auth.append("and")

        elif token.shape_ in t_const.NAME_SHAPES:
            if len(token) == 1:
                auth.append(token.text + ".")
            else:
                auth.append(token.text)

        elif token._.term in LOWER_RANK:
            taxon.append(RANK_ABBREV.get(token.lower_, token.lower_))
            rank = RANK_REPLACE.get(token.lower_, token.text)
            next_is_lower_taxon = True

        elif next_is_lower_taxon:
            taxon.append(token.lower_)
            next_is_lower_taxon = False

        token._.flag = "taxon"

    ent._.data["taxon"] = " ".join(taxon)
    ent._.data["rank"] = rank
    ent._.data["authority"] = auth
    ent._.relabel = "taxon"

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc("rename_taxon_match")
def rename_taxon_match(ent):
    rank = ""

    for token in ent:

        if token._.flag == "taxon_data":
            ent._.data = token._.data

        elif token._.term in ANY_RANK:
            rank = RANK_REPLACE.get(token.lower_, token.lower_)

    if rank:
        ent._.data["rank"] = rank

    ent._.relabel = "taxon"

    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"
