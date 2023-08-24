import logging
import sqlite3
import sys

from .db import db


def validate_trait_set(database, trait_set):
    with db.connect(database) as cxn:
        cxn.row_factory = sqlite3.Row
        rows = db.select(cxn, "select distinct trait_set from traits", one_column=True)
        all_trait_sets = list(rows)

    if trait_set in all_trait_sets:
        return

    logging.error(f"{trait_set} is not a valid trait set.")
    logging.error("Valid trait sets are:")
    logging.error(", ".join(all_trait_sets))
    sys.exit()


def validate_ocr_set(database, ocr_set):
    with db.connect(database) as cxn:
        cxn.row_factory = sqlite3.Row
        rows = db.select(cxn, "select distinct ocr_set from ocr_texts", one_column=True)
        all_ocr_sets = list(rows)

    if ocr_set in all_ocr_sets:
        return

    logging.error(f"{ocr_set} is not a valid OCR set.")
    logging.error("Valid OCR sets are:")
    logging.error(", ".join(all_ocr_sets))
    sys.exit()
