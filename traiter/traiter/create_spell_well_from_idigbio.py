#!/usr/bin/env python3
import argparse
import logging
import sqlite3
import textwrap
import zipfile
from collections import Counter
from pathlib import Path

import pandas as pd
import regex as re
from tqdm import tqdm

from pylib import log, spell_well
from pylib.rules import terms

CHUNK = 1_000_000

IS_WORD = re.compile(r"\p{L}+")


FIELDS = [
    "dwc:associatedOrganisms",
    "dwc:associatedTaxa",
    "dwc:behavior",
    "dwc:class",
    "dwc:county",
    "dwc:eventRemarks",
    "dwc:family",
    "dwc:fieldNotes",
    "dwc:genus",
    "dwc:group",
    "dwc:habitat",
    "dwc:identificationRemarks",
    "dwc:infraspecificEpithet",
    "dwc:island",
    "dwc:islandGroup",
    "dwc:lifeStage",
    "dwc:locality",
    "dwc:locationRemarks",
    "dwc:municipality",
    "dwc:occurrenceDetails",
    "dwc:occurrenceRemarks",
    "dwc:order",
    "dwc:organismRemarks",
    "dwc:reproductiveCondition",
    "dwc:scientificName",
    "dwc:sex",
    "dwc:specificEpithet",
    "dwc:stateProvince",
    "dwc:subgenus",
    "dwc:taxonRemarks",
    "dwc:verbatimTaxonRank",
    "dwc:vernacularName",
    "dwc:waterBody",
    "symbiota:verbatimScientificName",
]

CREATE = """
    create table if not exists vocab (
        word text,
        freq integer
    );
    create table if not exists misspellings (
        miss text,
        word text,
        dist integer,
        freq integer
    );
"""

INSERT_VOCAB = """insert into vocab (word, freq) values (?, ?);"""
INSERT_MISSPELLINGS = """
    insert into misspellings (miss, word, dist, freq) values (?, ?, ?, ?);
    """


def main():
    log.started()

    args = parse_args()

    freq = get_freq(args.idigbio_zip)
    freq = filter_freq(freq, args.min_freq, args.min_len)

    insert_vocab(freq, args.spell_well_db, args.delete_db)
    insert_misspellings(freq, args.spell_well_db, args.deletes)

    write_csv(args.spell_well_db)

    log.finished()


def write_csv(spell_well_db):
    with sqlite3.connect(spell_well_db) as cxn:
        logging.info("Exporting misspellings")
        df = pd.read_sql("select * from misspellings", cxn)
        path = Path(terms.__file__).parent / "misspellings.zip"
        df.to_csv(path, index=False)

        logging.info("Exporting vocab")
        df = pd.read_sql("select * from vocab.", cxn)
        path = Path(terms.__file__).parent / "vocab.zip"
        df.to_csv(path, index=False)


def filter_freq(freq, min_freq, min_len):
    return {k: v for k, v in freq.items() if v >= min_freq and len(k) >= min_len}


def insert_misspellings(freq, spell_well_db, deletes):
    logging.info("Inserting misspellings")

    batch = []
    hits = set()

    ordered = sorted(freq.items(), key=lambda f: (-f[1], f[0]))

    for word, count in tqdm(ordered):
        if word not in hits:
            batch.append((word, word, 0, count))
            hits.add(word)

        for delete in (w for w in spell_well.deletes1(word) if keep(word, w)):
            if delete not in hits:
                batch.append((delete, word, 1, count))
                hits.add(delete)

        if deletes > 1:
            for delete in (w for w in spell_well.deletes2(word) if keep(word, w)):
                if delete not in hits:
                    batch.append((delete, word, 2, count))
                    hits.add(delete)

    with sqlite3.connect(spell_well_db) as cxn:
        cxn.executemany(INSERT_MISSPELLINGS, batch)


def keep(word: str, delete: str):
    if len(delete) < 1:
        return False
    if word.istitle() and not delete.istitle():
        return False
    if word.islower() and not delete.islower():
        return False
    if word.isupper() and not delete.isupper():
        return False
    return True


def insert_vocab(freq, spell_well_db, delete_db):
    logging.info("Inserting vocab")

    if delete_db:
        spell_well_db.unlink(missing_ok=True)

    with sqlite3.connect(spell_well_db) as cxn:
        cxn.executescript(CREATE)
        cxn.executemany(INSERT_VOCAB, freq.items())


def get_freq(idigbio_zip):
    freq = Counter()

    with zipfile.ZipFile(idigbio_zip) as zippy:
        with zippy.open("occurrence_raw.csv") as in_file:
            reader = pd.read_csv(
                in_file,
                dtype=str,
                keep_default_na=False,
                chunksize=CHUNK,
                usecols=FIELDS,
            )

            for df in tqdm(reader):
                for field in FIELDS:
                    words = " ".join(f for f in df[field] if f)
                    words = IS_WORD.findall(words)
                    freq.update(words)
    return freq


def explore(idigbio_zip):
    with zipfile.ZipFile(idigbio_zip) as zippy:
        names = zippy.namelist()
        for name in names:
            print(name)

        with zippy.open("occurrence.csv") as in_file:
            headers = in_file.readline()
        headers = (h.decode().strip() for h in sorted(headers.split(b",")))
        print("=" * 80)
        for header in headers:
            print(header)

        with zippy.open("occurrence_raw.csv") as in_file:
            headers = in_file.readline()
        headers = (h.decode().strip() for h in sorted(headers.split(b",")))
        print("=" * 80)
        for header in headers:
            print(header)


def parse_args() -> argparse.Namespace:
    description = """Build a spell_well DB from iDigBio data.
        This is for building a spell checker for iDigBio terms."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars="@",
    )

    arg_parser.add_argument(
        "--idigbio-zip",
        type=Path,
        metavar="PATH",
        required=True,
        help="""Get terms from this iDigBio data dump.""",
    )

    arg_parser.add_argument(
        "--spell-well-db",
        type=Path,
        metavar="PATH",
        required=True,
        help="""Create this Spell-Well SQLite DB.""",
    )

    arg_parser.add_argument(
        "--delete-db",
        action="store_true",
        help="""Delete the Spell-Well SQLite DB before adding records.""",
    )

    arg_parser.add_argument(
        "--min-freq",
        type=int,
        metavar="N",
        default=100,
        help="""A word must be seen this many times to make it into the DB.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--min-len",
        type=int,
        metavar="LEN",
        default=3,
        help="""A word must long to make it into the DB. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--deletes",
        choices=[1, 2],
        default=1,
        help="""How many deletes to record. (default: %(default)s)""",
    )

    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
