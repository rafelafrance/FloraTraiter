import spacy
from traiter.pylib.pipes import extensions, sentence, tokenizer
from traiter.pylib.rules.date_ import Date
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.habitat import Habitat
from traiter.pylib.rules.lat_long import LatLong
from traiter.pylib.rules.trs import TRS
from traiter.pylib.rules.utm import UTM

from flora.pylib.rules import delete_missing, job_id, post_process
from flora.pylib.rules.admin_unit import AdminUnit
from flora.pylib.rules.associated_taxon_label import AssociatedTaxonLabel
from flora.pylib.rules.color import Color
from flora.pylib.rules.count import Count
from flora.pylib.rules.duration import Duration
from flora.pylib.rules.flower_location import FlowerLocation
from flora.pylib.rules.flower_morphology import FlowerMorphology
from flora.pylib.rules.habit import Habit
from flora.pylib.rules.id_number import IdNumber
from flora.pylib.rules.job import Job
from flora.pylib.rules.leaf_duration import LeafDuration
from flora.pylib.rules.leaf_folding import LeafFolding
from flora.pylib.rules.locality import Locality
from flora.pylib.rules.margin import Margin
from flora.pylib.rules.morphology import Morphology
from flora.pylib.rules.name import Name
from flora.pylib.rules.odor import Odor
from flora.pylib.rules.part import Part
from flora.pylib.rules.part_linker import PartLinker
from flora.pylib.rules.part_location import PartLocation
from flora.pylib.rules.part_location_linker import PartLocationLinker
from flora.pylib.rules.plant_duration import PlantDuration
from flora.pylib.rules.range import Range
from flora.pylib.rules.reproduction import Reproduction
from flora.pylib.rules.sex import Sex
from flora.pylib.rules.sex_linker import SexLinker
from flora.pylib.rules.shape import Shape
from flora.pylib.rules.size import Size
from flora.pylib.rules.subpart import Subpart
from flora.pylib.rules.subpart_linker import SubpartLinker
from flora.pylib.rules.surface import Surface
from flora.pylib.rules.taxon import Taxon
from flora.pylib.rules.taxon_like import TaxonLike
from flora.pylib.rules.taxon_like_linker import TaxonLikeLinker
from flora.pylib.rules.venation import Venation
from flora.pylib.rules.woodiness import Woodiness

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

    Taxon.pipe(nlp, extend=2, overwrite=["habitat", "color"])

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

    post_process.pipe(nlp)

    return nlp
