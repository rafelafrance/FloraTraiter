from pathlib import Path

from spacy.language import Language
from spacy.util import registry
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

ASSOC_CSV = Path(__file__).parent / "terms" / "associated_taxon_terms.csv"
PRIMARY_RANKS = set(""" species subspecies variety subvariety form subform """.split())


def build(nlp: Language):
    add.term_pipe(nlp, name="assoc_taxon_terms", path=ASSOC_CSV)
    add.trait_pipe(
        nlp,
        name="assoc_taxon_patterns",
        compiler=associated_taxon_patterns(),
    )
    add.custom_pipe(nlp, registered="label_assoc_taxon")
    add.cleanup_pipe(nlp, name="assoc_taxon_cleanup")


def associated_taxon_patterns():
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


@registry.misc("assoc_taxon_label_match")
def locality_match(ent):
    ent._.data = {"assoc_taxon_label": ent.text.lower()}


@Language.component("label_assoc_taxon")
def label_assoc_taxon(doc):
    """Mark taxa in the document as either primary or associated."""
    primary_ok = True

    for ent in doc.ents:
        if ent.label_ == "assoc_taxon_label":
            primary_ok = False

        elif ent.label_ == "taxon":
            taxon = ent._.data["taxon"]
            rank = ent._.data["rank"]

            if primary_ok and rank in PRIMARY_RANKS and len(taxon.split()) > 1:
                primary_ok = False

            else:
                relabel_entity(ent, "associated_taxon")
                ent._.data["trait"] = "associated_taxon"
                ent._.data["associated_taxon"] = taxon
                del ent._.data["taxon"]

    return doc


def relabel_entity(ent, label):
    strings = ent.doc.vocab.strings
    if label not in strings:
        strings.add(label)
    ent.label = strings[label]
