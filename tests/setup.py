import traiter.traiter.pylib.darwin_core as t_dwc
from flora.pylib import pipeline
from traiter.traiter.pylib.util import compress

PIPELINE = pipeline.build()


def parse(text: str) -> list:
    text = compress(text)
    doc = PIPELINE(text)
    traits = [e._.trait for e in doc.ents]

    # from pprint import pp
    # pp(traits)

    return traits


def to_dwc(label: str, text: str):
    doc = PIPELINE(text)

    # Isolate the trait being tested
    for ent in doc.ents:
        if ent.label_ == label:
            dwc = t_dwc.DarwinCore()
            return ent._.trait.to_dwc(dwc).to_dict()

    return {}
