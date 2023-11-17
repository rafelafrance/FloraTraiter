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
from flora.pylib.traits import job_id
from flora.pylib.traits.admin_unit import AdminUnit
from flora.pylib.traits.associated_taxon_label import AssociatedTaxonLabel
from flora.pylib.traits.color import Color
from flora.pylib.traits.count import Count
from flora.pylib.traits.duration import Duration
from flora.pylib.traits.flower_location import FlowerLocation
from flora.pylib.traits.flower_morphology import FlowerMorphology
from flora.pylib.traits.habit import Habit
from flora.pylib.traits.id_number import IdNumber
from flora.pylib.traits.job import Job
from flora.pylib.traits.leaf_duration import LeafDuration
from flora.pylib.traits.leaf_folding import LeafFolding
from flora.pylib.traits.locality import Locality
from flora.pylib.traits.margin import Margin
from flora.pylib.traits.morphology import Morphology
from flora.pylib.traits.name import Name
from flora.pylib.traits.odor import Odor
from flora.pylib.traits.part import Part
from flora.pylib.traits.part_linker import PartLinker
from flora.pylib.traits.part_location import PartLocation
from flora.pylib.traits.part_location_linker import PartLocationLinker
from flora.pylib.traits.plant_duration import PlantDuration
from flora.pylib.traits.range import Range
from flora.pylib.traits.reproduction import Reproduction
from flora.pylib.traits.sex import Sex
from flora.pylib.traits.sex_linker import SexLinker
from flora.pylib.traits.shape import Shape
from flora.pylib.traits.size import Size
from flora.pylib.traits.subpart import Subpart
from flora.pylib.traits.subpart_linker import SubpartLinker
from flora.pylib.traits.surface import Surface
from flora.pylib.traits.taxon import Taxon
from flora.pylib.traits.taxon_like import TaxonLike
from flora.pylib.traits.taxon_like_linker import TaxonLikeLinker
from flora.pylib.traits.venation import Venation
from flora.pylib.traits.woodiness import Woodiness

# from traiter.pylib.pipes import debug


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_md", exclude=["ner"])

    tokenizer.setup_tokenizer(nlp)

    config = {"base_model": "en_core_web_md"}
    nlp.add_pipe(sentence.SENTENCES, config=config, before="parser")

    Date.pipe(nlp)

    Part.pipe(nlp)
    Subpart.pipe(nlp)

    Elevation.pipe(nlp)
    LatLong.pipe(nlp)
    TRS.pipe(nlp)
    UTM.pipe(nlp)

    Color.pipe(nlp)
    Habitat.pipe(nlp)

    Duration.pipe(nlp)
    FlowerLocation.pipe(nlp)
    FlowerMorphology.pipe(nlp)
    LeafDuration.pipe(nlp)
    LeafFolding.pipe(nlp)
    Morphology.pipe(nlp)
    Odor.pipe(nlp)
    PlantDuration.pipe(nlp)
    Reproduction.pipe(nlp)
    Sex.pipe(nlp)
    Venation.pipe(nlp)
    Woodiness.pipe(nlp)

    IdNumber.pipe(nlp)
    Name.pipe(nlp, overwrite=["subpart", "color", "admin_unit"])
    Job.pipe(nlp)
    job_id.pipe(nlp)

    Range.pipe(nlp)
    Size.pipe(nlp)
    Count.pipe(nlp)

    Habit.pipe(nlp)
    Margin.pipe(nlp)
    Shape.pipe(nlp)
    Surface.pipe(nlp)

    AdminUnit.pipe(nlp, overwrite=["color"])

    Taxon.pipe(nlp, extend=2, overwrite=["habitat", "color"], auth_keep=["not_name"])

    PartLocation.pipe(nlp)
    TaxonLike.pipe(nlp)

    PartLinker.pipe(nlp)
    SubpartLinker.pipe(nlp)
    SexLinker.pipe(nlp)
    PartLocationLinker.pipe(nlp)
    TaxonLikeLinker.pipe(nlp)

    delete_missing.pipe(nlp)

    AssociatedTaxonLabel.pipe(nlp)

    Locality.pipe(nlp)

    return nlp
