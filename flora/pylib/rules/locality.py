import os
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import traiter.pylib.const as t_const
import traiter.pylib.darwin_core as t_dwc
from spacy.language import Language
from spacy.util import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.rules.base import Base

USE_MOCK_DATA = 0


@dataclass(eq=False)
class Locality(Base):
    # Class vars ----------
    # Traits at ends of locality phrases
    outer_traits: ClassVar[list[str]] = " habitat admin_unit subpart count".split()

    all_traits: ClassVar[list[str]] = [*outer_traits, "color"]

    punct: ClassVar[list[str]] = (
        t_const.COLON + t_const.COMMA + t_const.DASH + t_const.SLASH
    )

    min_len: ClassVar[int] = 4
    # ---------------------

    locality: str = None
    labeled: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(verbatimLocality=self.locality)

    @property
    def key(self) -> str:
        return t_dwc.DarwinCore.ns("verbatimLocality")

    @classmethod
    def pipe(cls, nlp: Language):
        default_labels = {
            "locality_terms": "loc",
            "mock_locality_terms": "loc",
        }
        add.term_pipe(
            nlp,
            name="locality_terms",
            path=cls.get_csvs(),
            default_labels=default_labels,
        )

        add.trait_pipe(nlp, name="locality_patterns", compiler=cls.locality_patterns())

        add.custom_pipe(nlp, registered="prune_localities")

        for i in range(1, 5):
            add.trait_pipe(
                nlp,
                name=f"extend_locality{i}",
                compiler=cls.extend_locality(),
                overwrite=["locality", *cls.all_traits],
            )

        add.trait_pipe(
            nlp,
            name="end_locality",
            compiler=cls.end_locality(),
            overwrite=["locality", *cls.all_traits],
        )

        add.cleanup_pipe(nlp, name="locality_cleanup")

    @classmethod
    def locality_patterns(cls):
        decoder = {
            ",": {"TEXT": {"IN": cls.punct}},
            "'s": {"POS": "PART"},
            "9": {"LIKE_NUM": True},
            "and": {"POS": {"IN": "ADP AUX CCONJ DET NUM SCONJ SPACE".split()}},
            "label": {"ENT_TYPE": "loc_label"},
            "loc": {"ENT_TYPE": "loc"},
            "sp": {"IS_SPACE": True},
            "trait": {"ENT_TYPE": {"IN": cls.all_traits}},
            "word": {"IS_ALPHA": True},
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
                    "9? loc+ word loc+ 9?",
                ],
            ),
        ]

    @classmethod
    def extend_locality(cls):
        return [
            Compiler(
                label="locality",
                on_match="locality_match",
                keep="locality",
                decoder={
                    ",": {"TEXT": {"IN": cls.punct}},
                    "9": {"LIKE_NUM": True},
                    "and": {"POS": {"IN": "ADP AUX CCONJ DET NUM SCONJ SPACE".split()}},
                    "loc": {"ENT_TYPE": "loc"},
                    "locality": {"ENT_TYPE": "locality"},
                    "rt": {"LOWER": {"REGEX": r"^\w[\w.]{,2}$"}},
                    "sent_start": {"IS_SENT_START": True},
                    "trait": {"ENT_TYPE": {"IN": cls.all_traits}},
                    "word": {"IS_ALPHA": True},
                },
                patterns=[
                    "sent_start+ 9?  ,? locality+",
                    "locality+   rt* ,? rt* ,? rt+",
                    "            rt* ,? rt* ,? rt+      locality+",
                    "locality+   word ,? 9? ,? trait*   locality+",
                    "locality+   word? ,? and? trait* and? ,? locality+",
                    "locality+   word? ,? and? trait* and? ,? loc+",
                    "loc+        word? ,? and? trait* and? ,? locality+",
                ],
            ),
        ]

    @classmethod
    def end_locality(cls):
        decoder = {
            ",": {"TEXT": {"IN": cls.punct}},
            ".": {"TEXT": {"IN": t_const.DOT + t_const.SEMICOLON + t_const.Q_MARK}},
            "9": {"LIKE_NUM": True},
            "not_eol": {"LOWER": {"REGEX": r"^[^\n\r;.]+$"}},
            "label": {"ENT_TYPE": "loc_label"},
            "locality": {"ENT_TYPE": "locality"},
            "in_sent": {"IS_SENT_START": False},
            "sent_start": {"IS_SENT_START": True},
            "sp": {"IS_SPACE": True},
            "trait": {"ENT_TYPE": {"IN": cls.outer_traits}},
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
                    "label+ ,? in_sent+ .",
                ],
            ),
        ]

    @staticmethod
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

    @classmethod
    def locality_match(cls, ent):
        if all(len(t.text) < cls.min_len for t in ent):
            raise reject_match.RejectMatch

        loc = ent.text.lstrip("(")
        loc = " ".join(loc.split())
        return cls.from_ent(ent, locality=loc)

    @classmethod
    def labeled_locality_match(cls, ent):
        i = 0
        for i, token in enumerate(ent):
            if token._.term != "loc_label":
                break
        return cls.from_ent(ent, locality=ent[i:].text, labeled=True)


@registry.misc("locality_match")
def locality_match(ent):
    return Locality.locality_match(ent)


@registry.misc("labeled_locality_match")
def labeled_locality_match(ent):
    return Locality.labeled_locality_match(ent)


@Language.component("prune_localities")
def prune_localities(doc):
    if USE_MOCK_DATA:  # Don't prune localities when testing
        return doc

    ents = []
    add_locality = False

    has_taxon = any(e._.trait and e._.trait.trait == "taxon" for e in doc.ents)

    for i, ent in enumerate(doc.ents):
        if not ent._.trait:
            continue

        trait = ent._.trait.trait

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
            if ent._.trait.labeled:
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
