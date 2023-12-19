from traiter.traiter.pylib import pipeline
from traiter.traiter.pylib.darwin_core import DarwinCore
from traiter.traiter.pylib.util import compress

PIPELINE = pipeline.build()


def parse(text: str) -> list:
    text = compress(text)
    doc = PIPELINE(text)

    traits = [e._.trait for e in doc.ents]

    return traits


def to_dwc(label: str, text: str):
    doc = PIPELINE(text)

    # Isolate the trait being tested
    for ent in doc.ents:
        if ent.label_ == label:
            dwc = DarwinCore()
            return ent._.trait.to_dwc(dwc).to_dict()

    return {}
