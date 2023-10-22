from traiter.pylib.util import compress

from flora.pylib import pipeline

PIPELINE = pipeline.build()


def test(text: str) -> list[dict]:
    text = compress(text)
    doc = PIPELINE(text)
    traits = [e._.trait for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
