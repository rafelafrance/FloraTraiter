import spacy

from traiter.traiter.pylib.pipes import extensions
from traiter.traiter.pylib.pipes import sentence
from traiter.traiter.pylib.pipes import tokenizer
from traiter.traiter.pylib.rules.color import Color
from traiter.traiter.pylib.rules.date_ import Date
from traiter.traiter.pylib.rules.elevation import Elevation
from traiter.traiter.pylib.rules.habitat import Habitat
from traiter.traiter.pylib.rules.lat_long import LatLong
from traiter.traiter.pylib.rules.trs import TRS
from traiter.traiter.pylib.rules.utm import UTM


def build():
    extensions.add_extensions()

    nlp = spacy.load("en_core_web_sm", exclude=["ner", "lemmatizer", "tok2vec"])

    tokenizer.setup_tokenizer(nlp)

    nlp.add_pipe(sentence.SENTENCES, before="parser")

    Color.pipe(nlp)
    Date.pipe(nlp)
    Elevation.pipe(nlp)
    LatLong.pipe(nlp)
    Habitat.pipe(nlp)
    TRS.pipe(nlp)
    UTM.pipe(nlp)

    return nlp
