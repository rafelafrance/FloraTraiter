import json

from tqdm import tqdm
from traiter.pylib import util

from ..db import db
from . import pipeline


def ner(args):
    with db.connect(args.database) as cxn:
        run_id = db.insert_run(cxn, args)
        db.canned_delete(cxn, "traits", trait_set=args.trait_set)

    nlp = pipeline.build()

    with db.connect(args.database) as cxn:
        records = db.canned_select(cxn, "ocr_texts", ocr_set=args.ocr_set)

    if args.limit:
        records = records[args.offset : args.limit + args.offset]

    if args.label_id:
        records = [r for r in records if r["label_id"] == args.label_id]

    with db.connect(args.database) as cxn:
        for ocr_text in tqdm(records, desc="parse"):
            text = util.shorten(ocr_text["ocr_text"])

            batch = []

            doc = nlp(text)

            traits = [e._.data for e in doc.ents]

            for trait in traits:
                batch.append(
                    {
                        "trait_set": args.trait_set,
                        "ocr_id": ocr_text["ocr_id"],
                        "trait": trait["trait"],
                        "data": json.dumps(trait),
                    }
                )
            db.canned_insert(cxn, "traits", batch)

        db.update_run_finished(cxn, run_id)
