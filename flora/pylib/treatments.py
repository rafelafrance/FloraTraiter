from tqdm import tqdm

from flora.pylib.treatment import Treatment

from . import pipeline


class Treatments:
    def __init__(self, args):
        self.treatments: list[Treatment] = self.get_treatments(args)
        self.nlp = pipeline.build()

    @staticmethod
    def get_treatments(args):
        labels = [Treatment(p) for p in sorted(args.text_dir.glob("*"))]

        if args.limit:
            labels = labels[args.offset : args.limit + args.offset]

        return labels

    def parse(self):
        for lb in tqdm(self.treatments, desc="parse"):
            lb.parse(self.nlp)
