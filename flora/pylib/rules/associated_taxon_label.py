from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.rules.base import Base


@dataclass(eq=False)
class AssociatedTaxonLabel(Base):
    # Class vars ----------
    assoc_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "associated_taxon_terms.csv"
    )
    primary_ranks: ClassVar[set[str]] = set(
        "species subspecies variety subvariety form subform".split(),
    )
    # ---------------------

    label: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="assoc_taxon_terms", path=cls.assoc_csv)
        add.trait_pipe(
            nlp,
            name="assoc_taxon_patterns",
            compiler=cls.associated_taxon_patterns(),
        )
        add.custom_pipe(nlp, registered="label_assoc_taxon")
        add.cleanup_pipe(nlp, name="assoc_taxon_cleanup")

    @classmethod
    def associated_taxon_patterns(cls):
        return [
            Compiler(
                label="assoc_taxon_label",
                on_match="assoc_taxon_label_match",
                decoder={
                    "assoc": {"ENT_TYPE": "assoc"},
                    "label": {"ENT_TYPE": "assoc_label"},
                },
                keep="assoc_taxon_label",
                patterns=[
                    "assoc label",
                ],
            ),
        ]

    @classmethod
    def assoc_taxon_label_match(cls, ent):
        return cls.from_ent(ent, label=ent.text.lower())

    @classmethod
    def label_assoc_taxon(cls, doc):
        primary_ok = True

        for ent in doc.ents:
            if ent.label_ == "assoc_taxon_label":
                primary_ok = False

            elif ent.label_ == "taxon":
                taxon = ent._.trait.taxon
                rank = ent._.trait.rank

                if primary_ok and rank in cls.primary_ranks and len(taxon.split()) > 1:
                    primary_ok = False

                else:
                    ent._.trait.associated = True

        return doc


@registry.misc("assoc_taxon_label_match")
def locality_match(ent):
    return AssociatedTaxonLabel.assoc_taxon_label_match(ent)


@Language.component("label_assoc_taxon")
def label_assoc_taxon(doc):
    return AssociatedTaxonLabel.label_assoc_taxon(doc)
