import spacy
from traiter.pylib.pipes import extensions
from traiter.pylib.pipes import sentence
from traiter.pylib.pipes import tokenizer
from traiter.pylib.traits import color
from traiter.pylib.traits import date_
from traiter.pylib.traits import elevation
from traiter.pylib.traits import geocoordinates
from traiter.pylib.traits import habitat

from flora.pylib.traits import admin_unit
from flora.pylib.traits import associated_taxon
from flora.pylib.traits import delete_missing
from flora.pylib.traits import habit
from flora.pylib.traits import link_location
from flora.pylib.traits import link_part
from flora.pylib.traits import link_sex
from flora.pylib.traits import link_taxon_like
from flora.pylib.traits import locality
from flora.pylib.traits import margin
from flora.pylib.traits import misc
from flora.pylib.traits import numeric
from flora.pylib.traits import part
from flora.pylib.traits import part_location
from flora.pylib.traits import person
from flora.pylib.traits import shape
from flora.pylib.traits import surface
from flora.pylib.traits import taxon
from flora.pylib.traits import taxon_like


def build(model_path=None):
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    config = {"base_model": "en_core_web_md"}
    nlp.add_pipe(sentence.SENTENCES, config=config, before="parser")

    date_.build(nlp)

    part.build(nlp)

    elevation.build(nlp)
    geocoordinates.build(nlp)

    color.build(nlp)
    habitat.build(nlp)

    misc.build(nlp)

    numeric.build(nlp)
    person.build(nlp, overwrite=["subpart", "color", "count", "admin_unit"])

    habit.build(nlp)
    margin.build(nlp)
    shape.build(nlp)
    surface.build(nlp)

    admin_unit.build(nlp, overwrite=["color"])
    taxon.build(nlp, extend=2, overwrite=["habitat", "color"], auth_keep=["not_name"])

    part_location.build(nlp)
    taxon_like.build(nlp)

    link_part.build(nlp)
    link_sex.build(nlp)
    link_location.build(nlp)
    link_taxon_like.build(nlp)

    delete_missing.build(nlp)

    associated_taxon.build(nlp)

    locality.build(nlp)

    if model_path:
        nlp.to_disk(model_path)

    return nlp


def load(model_path):
    extensions.add_extensions()
    nlp = spacy.load(model_path)
    return nlp
