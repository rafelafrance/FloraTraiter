import spacy

from traiter.pylib.pipes import extensions, sentence, tokenizer
from traiter.pylib.rules.color import Color
from traiter.pylib.rules.date_ import Date
from traiter.pylib.rules.elevation import Elevation
from traiter.pylib.rules.habitat import Habitat
from traiter.pylib.rules.lat_long import LatLong
from traiter.pylib.rules.trs import TRS
from traiter.pylib.rules.utm import UTM


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
