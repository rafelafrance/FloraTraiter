from tqdm import tqdm

from flora.pylib.treatment import Treatment

from . import pipeline


class Treatments:
    def __init__(self, args):
        self.treatments: list[Treatment] = self.get_treatments(args)
        self.nlp = pipeline.build()

    @staticmethod
    def get_treatments(args):
        treatments = [Treatment(p) for p in sorted(args.text_dir.glob("*"))]

        if args.limit:
            treatments = treatments[args.offset : args.limit + args.offset]

        return treatments

    @staticmethod
    def get_image_paths(args):
        images = {}
        if args.image_dir:
            images = {p.stem: p for p in args.image_dir.glob("*")}
        return images

    def parse(self):
        for treat in tqdm(self.treatments, desc="parse"):
            treat.parse(self.nlp)
