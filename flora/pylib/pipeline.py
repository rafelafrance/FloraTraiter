import spacy
from traiter.pylib.pipes import extensions
from traiter.pylib.pipes import tokenizer
from traiter.pylib.traits import color
from traiter.pylib.traits import date_
from traiter.pylib.traits import elevation
from traiter.pylib.traits import geocoordinates
from traiter.pylib.traits import habitat

from .traits import delete_missing
from .traits import habit
from .traits import link_location
from .traits import link_part
from .traits import link_sex
from .traits import link_taxon_like
from .traits import margin
from .traits import misc
from .traits import numeric
from .traits import part
from .traits import part_location
from .traits import shape
from .traits import surface
from .traits import taxon
from .traits import taxon_like


def build(model_path=None):
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_sm", exclude=["parser", "ner"])

    tokenizer.setup_tokenizer(nlp)

    taxon.build(nlp, extend=2)
    misc.build(nlp)
    part.build(nlp)
    numeric.build(nlp)

    color.build(nlp)
    date_.build(nlp)
    elevation.build(nlp)
    habitat.build(nlp)
    geocoordinates.build(nlp)

    habit.build(nlp)
    margin.build(nlp)
    shape.build(nlp)
    surface.build(nlp)

    part_location.build(nlp)
    taxon_like.build(nlp)

    link_part.build(nlp)
    link_sex.build(nlp)
    link_location.build(nlp)
    link_taxon_like.build(nlp)

    delete_missing.build(nlp)

    if model_path:
        nlp.to_disk(model_path)

    return nlp


def load(model_path):
    extensions.add_extensions()
    nlp = spacy.load(model_path)
    return nlp
