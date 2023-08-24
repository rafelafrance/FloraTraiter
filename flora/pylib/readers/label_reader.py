import json
from collections import namedtuple

from traiter.pylib.util import shorten

from ..db import db

START = -1

TraitsInText = namedtuple("TraitsInText", "label_id text traits data")


class LabelReader:
    def __init__(self, args):
        self.labels = self.read_traits(args.database, args.trait_set)

    @staticmethod
    def read_traits(database, trait_set):
        labels = []
        prev_label_id = START
        record = TraitsInText(label_id=START, text="", traits=[], data={})

        with db.connect(database) as cxn:
            all_traits = db.canned_select(cxn, "traits", trait_set=trait_set)

        for trait in all_traits:
            if trait["label_id"] != prev_label_id:
                if record.label_id != START:
                    labels.append(record)

                record = TraitsInText(
                    label_id=trait["label_id"],
                    text=shorten(trait["ocr_text"]),
                    traits=[],
                    data=trait,
                )
                prev_label_id = record.label_id

            record.traits.append(json.loads(trait["data"]))

        if record.label_id != START:
            labels.append(record)

        return labels
