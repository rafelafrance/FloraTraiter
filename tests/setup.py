from traiter.pylib.util import shorten

from flora.pylib.pipelines import full_pipeline
from flora.pylib.pipelines import small_pipeline

SMALL_PIPELINE = small_pipeline.build()
PIPELINE = full_pipeline.build()


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = SMALL_PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits


def test2(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
