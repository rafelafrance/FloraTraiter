"""All of the traits."""

from lib.traits.sex_trait import SexTrait
from lib.traits.body_mass_trait import BodyMassTrait
from lib.traits.life_stage_trait import LifeStageTrait
from lib.traits.ear_length_trait import EarLengthTrait
from lib.traits.tail_length_trait import TailLengthTrait
from lib.traits.testes_size_trait import TestesSizeTrait
from lib.traits.testes_state_trait import TestesStateTrait
from lib.traits.total_length_trait import TotalLengthTrait
from lib.traits.hind_foot_length_trait import HindFootLengthTrait


TRAIT_LIST = [
    ('sex', SexTrait),
    ('body_mass', BodyMassTrait),
    ('life_stage', LifeStageTrait),
    ('total_length', TotalLengthTrait),
    ('tail_length', TailLengthTrait),
    ('hind_foot_length', HindFootLengthTrait),
    ('ear_length', EarLengthTrait),
    ('testes_size', TestesSizeTrait),
    ('testes_state', TestesStateTrait),
]

TRAIT_NAMES = [t[0] for t in TRAIT_LIST]
TRAIT_DICT = {k: v for k, v in TRAIT_LIST}
