#!/usr/bin/env python3
"""Mostly use binomials names for species and monomials for higher and lower taxa."""
import argparse
import csv
import logging
import sqlite3
import sys
import textwrap
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile

import regex
from pylib import const
from tqdm import tqdm
from traiter.pylib import log
from traiter.pylib import term_util as tu
from traiter.pylib.traits import terms as t_terms

from plants.pylib.traits import terms

ITIS_SPECIES_ID = 220


@dataclass
class Record:
    label: str
    pattern: str
    ranks: str


class Ranks:
    def __init__(self):
        rank_csv = Path(terms.__file__).parent / "rank_terms.csv"
        with open(rank_csv) as term_file:
            reader = csv.DictReader(term_file)
            self.ranks = list(reader)
        self.id2rank = {int(r["rank_id"]): r["replace"] for r in self.ranks}
        self.rank_names = tu.term_data(rank_csv, "replace")
        self.lower = {r for i, r in self.id2rank.items() if i > ITIS_SPECIES_ID}
        self.higher = {r for i, r in self.id2rank.items() if i < ITIS_SPECIES_ID}

    def normalize_rank(self, rank):
        rank = rank.lower()
        return self.rank_names.get(rank, "")


class Taxa:
    def __init__(self, ranks):
        self.ranks = ranks
        self.taxon = defaultdict(set)  # Ranks for each term
        self.valid_pattern = regex.compile(r"^\p{L}[\p{L}\s'.-]*\p{L}$")

    def add_taxon_and_rank(self, pattern, rank):
        words = pattern.split()

        if rank not in self.ranks.rank_names:
            return

        if len(words) == 1:
            self.taxon[pattern.lower()].add(rank)

        elif len(words) >= 2:
            self.add_binomial(words)
            rank = rank
            for word in words[2:]:
                if new_rank := self.ranks.rank_names.get(word):
                    rank = new_rank
                else:
                    self.taxon[word.lower()].add(rank)

    def add_binomial(self, words):
        binomial = f"{words[0].title()} {words[1].lower()}"
        genus = words[0].lower()
        species = words[1].lower()
        self.taxon[binomial].add("species")
        self.taxon[genus].add("genus")
        self.taxon[species].add("species")

    def add_taxa_and_ranks(self, pattern, ranks):
        for rank in ranks:
            self.add_taxon_and_rank(pattern, rank)

    def remove_problem_taxa(self, show_rejected):
        """Some taxa interfere with other parses."""
        new = {}

        all_csvs = [
            Path(t_terms.__file__).parent / "color_terms.csv",
            Path(t_terms.__file__).parent / "habitat_terms.csv",
            Path(t_terms.__file__).parent / "us_location_terms.csv",
            Path(terms.__file__).parent / "habit_terms.csv",
            Path(terms.__file__).parent / "numeric_terms.csv",
            Path(terms.__file__).parent / "part_terms.csv",
            Path(terms.__file__).parent / "rank_terms.csv",
            Path(terms.__file__).parent / "shape_terms.csv",
            Path(terms.__file__).parent / "surface_terms.csv",
        ]

        problem_words = {"dummy", "mosaic", "name", "temp", "uncertain", "unknown"}

        rows = tu.read_terms(all_csvs)

        problem_taxa = set("end erica flora floral harms lake may phoenix side".split())
        problem_taxa |= {t["pattern"].lower() for t in rows}

        taxa = sorted(self.taxon.items())

        for taxon_, rank in taxa:
            words = taxon_.split()

            if taxon_.lower() in problem_taxa:
                print(f"Removed {taxon_} {rank}")
                continue

            if any(w.lower() in problem_words for w in words):
                print(f"Removed {taxon_} {rank}")
                continue

            if not self.valid_pattern.match(taxon_):
                if show_rejected:
                    print(f"Removed {taxon_} {rank}")
                continue

            if len(taxon_) < const.MIN_TAXON_LEN:
                if show_rejected:
                    print(f"Removed {taxon_} {rank}")
                continue

            if any(len(w) < const.MIN_TAXON_WORD_LEN for w in words):
                if show_rejected:
                    print(f"Removed {taxon_} {rank}")
                continue

            new[taxon_] = rank

        self.taxon = new


def main():
    log.started()

    ranks = Ranks()
    taxa = Taxa(ranks)

    args = parse_args()

    read_taxa(args, taxa)

    taxa.remove_problem_taxa(args.show_rejected)

    records = build_records(taxa)
    counts = count_ranks(records)
    sort_ranks(counts, records, taxa)

    write_csv(records)

    log.finished()


def count_ranks(records):
    counts = defaultdict(int)
    for record in records:
        ranks = record.ranks.split()
        for rank in ranks:
            counts[rank] += 1
    return counts


def sort_ranks(counts, records, taxa):
    logging.info("Sorting ranks")

    for record in records:
        keys = []

        for rank in record.ranks.split():
            if rank in taxa.ranks.higher:
                keys.append((1, -counts[rank], rank))
            elif rank in taxa.ranks.lower:
                keys.append((2, -counts[rank], rank))
            else:
                keys.append((3, -counts[rank], rank))

        record.ranks = " ".join([k[2] for k in sorted(keys)])


def build_records(taxa):
    logging.info("Building records")

    records = []

    for taxon_, ranks in taxa.taxon.items():
        word_count = len(taxon_.split())
        if word_count < 3:
            records.append(
                Record(
                    label="monomial" if word_count == 1 else "binomial",
                    pattern=taxon_.lower(),
                    ranks=" ".join(ranks),
                )
            )
        else:
            logging.error(f"Parse error: {taxon_}")
            sys.exit(1)

    return records


def write_csv(rows):
    monomial_csv = const.DATA_DIR / "monomial_terms.csv"
    binomial_csv = const.DATA_DIR / "binomial_terms.csv"
    monomial_zip = Path(terms.__file__).parent / "monomial_terms.zip"
    binomial_zip = Path(terms.__file__).parent / "binomial_terms.zip"

    with open(monomial_csv, "w") as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(""" pattern ranks """.split())
        for r in rows:
            if r.label == "monomial":
                writer.writerow([r.pattern, r.ranks])
    with ZipFile(monomial_zip, "w", ZIP_DEFLATED, compresslevel=9) as zippy:
        zippy.write(monomial_csv, arcname=monomial_csv.name)

    with open(binomial_csv, "w") as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(""" pattern """.split())
        for r in rows:
            if r.label == "binomial":
                writer.writerow([r.pattern])
    with ZipFile(binomial_zip, "w", ZIP_DEFLATED, compresslevel=9) as zippy:
        zippy.write(binomial_csv, arcname=binomial_csv.name)


def read_taxa(args, taxa):
    if args.itis_db:
        read_itis_taxa(args.itis_db, taxa)

    if args.wcvp_file:
        read_wcvp_taxa(args.wcvp_file, taxa)

    if args.wfot_tsv:
        read_wfot_taxa(args.wfot_tsv, taxa)

    if args.other_taxa_csv:
        read_other_taxa(args.other_taxa_csv, taxa)


def read_other_taxa(other_taxa_csv, taxa):
    with open(other_taxa_csv) as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            for rank in set(row["ranks"].split()):
                taxa.add_taxon_and_rank(row["pattern"], rank)


def read_wfot_taxa(wfot_tsv, taxa):
    with open(wfot_tsv) as in_file:
        reader = csv.DictReader(in_file, delimiter="\t")
        for row in tqdm(reader, desc="wfot"):
            rank = taxa.ranks.normalize_rank(row["taxonRank"])
            pattern = row["scientificName"]
            taxa.add_taxon_and_rank(pattern, rank)


def read_wcvp_taxa(wcvp_file, taxa):
    with open(wcvp_file) as in_file:
        reader = csv.DictReader(in_file, delimiter="|")
        for row in tqdm(reader, desc="wcvp"):
            rank = taxa.ranks.normalize_rank(row["taxonrank"])
            pattern = row["scientfiicname"]
            taxa.add_taxon_and_rank(pattern, rank)


def read_itis_taxa(itis_db, taxa):
    itis_kingdom_id = 3

    with sqlite3.connect(itis_db) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select complete_name, rank_id from taxonomic_units where kingdom_id = ?"
        rows = [t for t in tqdm(cxn.execute(sql, (itis_kingdom_id,)), desc="itis")]

    for row in rows:
        rank, pattern = taxa.ranks.id2rank[row["rank_id"]], row["complete_name"]
        taxa.add_taxon_and_rank(pattern, rank)


def parse_args():
    description = """Build a database taxon patterns."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--itis-db",
        type=Path,
        metavar="PATH",
        help="""Get terms from this ITIS database.""",
    )

    arg_parser.add_argument(
        "--wcvp-file",
        type=Path,
        metavar="PATH",
        help="""Get terms from this WCVP file. It is '|' a separated CSV.""",
    )

    arg_parser.add_argument(
        "--wfot-tsv",
        type=Path,
        metavar="PATH",
        help="""Get terms from this WFO Taxonomic TSV.""",
    )

    arg_parser.add_argument(
        "--other-taxa-csv",
        type=Path,
        metavar="PATH",
        help="""Get even more taxa from this CSV file.""",
    )

    arg_parser.add_argument(
        "--show-rejected",
        action="store_true",
        help="""Print everything that is rejected from the CSV.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
