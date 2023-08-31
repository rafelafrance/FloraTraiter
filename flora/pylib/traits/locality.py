import os
from pathlib import Path

import traiter.pylib.const as t_const
from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

USE_MOCK_DATA = 0

# Traits at ends of locality phrases
OUTER_TRAITS = " habitat admin_unit subpart ".split()

ALL_TRAITS = [*OUTER_TRAITS, "color"]

PUNCT = t_const.COLON + t_const.COMMA + t_const.DASH + t_const.SLASH


def get_csvs():
    global USE_MOCK_DATA

    here = Path(__file__).parent / "terms"
    csvs = [
        here / "locality_terms.zip",
        here / "other_locality_terms.csv",
    ]

    try:
        USE_MOCK_DATA = int(os.getenv("MOCK_DATA"))
    except (TypeError, ValueError):
        USE_MOCK_DATA = 0

    if not csvs[0].exists or USE_MOCK_DATA:
        csvs = [
            here / "mock_locality_terms.csv",
            here / "other_locality_terms.csv",
        ]

    return csvs


def build(nlp: Language):
    default_labels = {
        "locality_terms": "loc",
        "mock_locality_terms": "loc",
    }
    add.term_pipe(
        nlp, name="locality_terms", path=get_csvs(), default_labels=default_labels
    )

    # add.debug_tokens(nlp)  # ##########################################

    add.trait_pipe(nlp, name="locality_patterns", compiler=locality_patterns())

    # add.debug_tokens(nlp)  # ##########################################

    add.custom_pipe(nlp, registered="prune_localities")

    for i in range(1, 5):
        # add.debug_tokens(nlp)  # ##########################################
        add.trait_pipe(
            nlp,
            name=f"extend_locality{i}",
            compiler=extend_locality(),
            overwrite=["locality", *ALL_TRAITS],
        )

    # add.debug_tokens(nlp)  # ##########################################

    add.trait_pipe(
        nlp,
        name="end_locality",
        compiler=end_locality(),
        overwrite=["locality", *ALL_TRAITS],
    )

    # add.debug_tokens(nlp)  # ##########################################

    add.cleanup_pipe(nlp, name="locality_cleanup")


def locality_patterns():
    decoder = {
        ",": {"TEXT": {"IN": PUNCT}},
        "'s": {"POS": "PART"},
        "9": {"LIKE_NUM": True},
        "and": {"POS": {"IN": "ADP AUX CCONJ DET NUM SCONJ SPACE".split()}},
        "loc": {"ENT_TYPE": "loc"},
        "sp": {"IS_SPACE": True},
        "trait": {"ENT_TYPE": {"IN": ALL_TRAITS}},
    }
    return [
        Compiler(
            label="locality",
            on_match="locality_match",
            keep="locality",
            decoder=decoder,
            patterns=[
                "9? loc+ 's?  loc+ 9?",
                "9? loc+ ,+   loc+ 9?",
                "9? loc+ and+ loc+ 9?",
                "9? loc+ and+ loc+ and+ loc+ 9?",
                "9? loc+ and+ loc+ and+ loc+ and+ loc+ 9?",
                "9? loc+ and+ loc+ and+ loc+ and+ loc+ and+ loc+ 9?",
                "9? loc+ trait 9?",
            ],
        ),
    ]


def extend_locality():
    return [
        Compiler(
            label="locality",
            on_match="locality_match",
            keep="locality",
            decoder={
                ",": {"TEXT": {"IN": PUNCT}},
                "9": {"LIKE_NUM": True},
                "and": {"POS": {"IN": "ADP AUX CCONJ DET NUM SCONJ SPACE".split()}},
                "loc": {"ENT_TYPE": "loc"},
                "locality": {"ENT_TYPE": "locality"},
                "rt": {"LOWER": {"REGEX": r"^\w[\w.]{,2}$"}},
                "sent_start": {"IS_SENT_START": True},
                "trait": {"ENT_TYPE": {"IN": ALL_TRAITS}},
                "word": {"IS_ALPHA": True},
            },
            patterns=[
                "sent_start+ 9?  ,? locality+",
                "locality+   rt* ,? rt* ,? rt+",
                "            rt* ,? rt* ,? rt+      locality+",
                "locality+   word ,? 9? ,? trait*   locality+",
                "locality+   ,? and? trait* and? ,? locality+",
                "locality+   ,? and? trait* and? ,? loc+",
                "loc+        ,? and? trait* and? ,? locality+",
            ],
        )
    ]


def end_locality():
    decoder = {
        ",": {"TEXT": {"IN": PUNCT}},
        ".": {"TEXT": {"IN": t_const.DOT + t_const.SEMICOLON}},
        "9": {"LIKE_NUM": True},
        "label": {"ENT_TYPE": "loc_label"},
        "locality": {"ENT_TYPE": "locality"},
        "in_sent": {"IS_SENT_START": False},
        "sent_start": {"IS_SENT_START": True},
        "sp": {"IS_SPACE": True},
        "trait": {"ENT_TYPE": {"IN": OUTER_TRAITS}},
        "word": {"IS_ALPHA": True},
    }
    return [
        Compiler(
            label="locality",
            on_match="locality_match",
            decoder=decoder,
            keep="locality",
            patterns=[
                "locality+ ,? sp? word? sp? trait+ .",
                "locality+ ,? sp? word? sp? 9+ .",
                "locality+ ,? sp? word+ sp? .",
            ],
        ),
        Compiler(
            label="labeled_locality",
            id="locality",
            on_match="labeled_locality_match",
            decoder=decoder,
            keep="locality",
            patterns=[
                "label+ in_sent+ .",
            ],
        ),
    ]


@registry.misc("locality_match")
def locality_match(ent):
    loc = ent.text.lstrip("(")
    loc = " ".join(loc.split())
    ent._.data = {"locality": loc}


@registry.misc("labeled_locality_match")
def labeled_locality_match(ent):
    i = 0
    for i, token in enumerate(ent):
        if token._.term != "loc_label":
            break
    ent._.data = {
        "locality": ent[i:].text,
        "labeled": True,
    }


@Language.component("prune_localities")
def prune_localities(doc):
    if USE_MOCK_DATA:  # Don't prune localities when testing
        return doc

    ents = []
    add_locality = False

    has_taxon = any(e._.data["trait"] == "taxon" for e in doc.ents)

    for i, ent in enumerate(doc.ents):
        trait = ent._.data["trait"]

        # Localities come after taxa
        if trait in ("taxon",):  # "admin_unit"):
            add_locality = True

        # Start localities when there is no taxon
        elif trait in ("associated_taxon",) and not has_taxon:
            add_locality = True

        # Localities are before collector etc.
        elif trait in ("collector", "date", "determiner") and i > len(doc.ents) // 2:
            add_locality = False

        elif trait == "locality":
            # Always keep labeled localities
            if ent._.data.get("labeled", False):
                pass

            # At beginning or end of label
            elif not add_locality:
                continue

            # Skip a name
            elif len(ent) <= 2 and len(ent[0]) <= 2 and ent[0].text[-1] == ".":
                continue

        ents.append(ent)

    doc.set_ents(sorted(ents, key=lambda e: e.start))
    return doc
