from tqdm import tqdm

from flora.pylib.treatment import Treatment

from .pipelines import flora_pipeline


class Treatments:
    def __init__(self, treatment_dir, limit, offset):
        self.treatments: list[Treatment] = self.get_treatments(
            treatment_dir, limit, offset
        )
        self.nlp = flora_pipeline.build()

    def __iter__(self):
        yield from self.treatments

    @staticmethod
    def get_treatments(treatment_dir, limit, offset):
        labels = [Treatment(p) for p in sorted(treatment_dir.glob("*"))]

        if limit:
            labels = labels[offset : limit + offset]

        return labels

    def parse(self):
        for lb in tqdm(self.treatments, desc="parse"):
            lb.parse(self.nlp)
