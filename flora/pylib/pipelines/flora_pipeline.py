import spacy
from traiter.pylib.pipes import extensions, sentence, tokenizer

from flora.pylib.rules import delete_missing, delete_too_far, post_process
from flora.pylib.rules.color import Color
from flora.pylib.rules.count import Count
from flora.pylib.rules.duration import Duration
from flora.pylib.rules.flower_location import FlowerLocation
from flora.pylib.rules.flower_morphology import FlowerMorphology
from flora.pylib.rules.habit import Habit
from flora.pylib.rules.leaf_duration import LeafDuration
from flora.pylib.rules.leaf_folding import LeafFolding
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

    Part.pipe(nlp)
    Subpart.pipe(nlp)

    Color.pipe(nlp)

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

    Name.pipe(nlp, overwrite=["subpart", "color", "admin_unit"])

    Range.pipe(nlp)
    Size.pipe(nlp)
    Count.pipe(nlp)

    Habit.pipe(nlp)
    Margin.pipe(nlp)
    Shape.pipe(nlp)
    Surface.pipe(nlp)

    Taxon.pipe(nlp, extend=2, overwrite=["habitat", "color"])

    PartLocation.pipe(nlp)
    TaxonLike.pipe(nlp)

    PartLinker.pipe(nlp)
    SubpartLinker.pipe(nlp)
    SexLinker.pipe(nlp)
    PartLocationLinker.pipe(nlp)
    TaxonLikeLinker.pipe(nlp)

    delete_missing.pipe(nlp)
    delete_too_far.pipe(nlp)

    post_process.pipe(nlp)

    return nlp
