import json
from collections import defaultdict

from tqdm import tqdm

from flora.pylib.pipelines import full_pipeline


def parse(args) -> dict[str, list]:
    paths = sorted(args.text_dir.glob("*"))

    nlp = full_pipeline.build()

    if args.limit:
        paths = paths[args.offset : args.limit + args.offset]

    if args.filter:
        paths = [p for p in paths if str(p).find(args.filter)]

    labels = defaultdict(list)

    for path in tqdm(paths, desc="parse"):
        with open(path) as f:
            text = f.read()

        doc = nlp(text)

        labels[str(path)] = [e._.data for e in doc.ents]

    return labels
