import spacy
from traiter.pylib.pipes import extensions
from traiter.pylib.pipes import sentence
from traiter.pylib.pipes import tokenizer
from traiter.pylib.traits.date_ import Date
from traiter.pylib.traits.elevation import Elevation
from traiter.pylib.traits.habitat import Habitat
from traiter.pylib.traits.lat_long import LatLong
from traiter.pylib.traits.trs import TRS
from traiter.pylib.traits.utm import UTM

from flora.pylib.traits import delete_missing
from flora.pylib.traits.admin_unit import AdminUnit
from flora.pylib.traits.associated_taxon import AssociatedTaxonLabel
from flora.pylib.traits.color import Color
from flora.pylib.traits.habit import Habit


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    config = {"base_model": "en_core_web_md"}
    nlp.add_pipe(sentence.SENTENCES, config=config, before="parser")

    Date.pipe(nlp)

    # part.build(nlp)

    Elevation.pipe(nlp)
    LatLong.pipe(nlp)
    TRS.pipe(nlp)
    UTM.pipe(nlp)

    Color.pipe(nlp)
    Habitat.pipe(nlp)

    # misc.build(nlp)

    # job.build(nlp, overwrite=["subpart", "color", "admin_unit"])
    # numeric.build(nlp)

    Habit.pipe(nlp)
    # margin.build(nlp)
    # shape.build(nlp)
    # surface.build(nlp)

    AdminUnit.pipe(nlp, overwrite=["color"])
    # taxon.build(nlp, extend=2, overwrite=["habitat", "color"], auth_keep=["not_name"])

    # location.build(nlp)
    # taxon_like.build(nlp)

    # link_part.build(nlp)
    # link_sex.build(nlp)
    # link_location.build(nlp)
    # link_taxon_like.build(nlp)

    delete_missing.pipe(nlp)

    AssociatedTaxonLabel.pipe(nlp)

    # locality.build(nlp)

    return nlp
