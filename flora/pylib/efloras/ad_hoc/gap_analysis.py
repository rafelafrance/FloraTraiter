"""Create a GAP analysis of traits vs taxon."""
import argparse
import sqlite3
import textwrap

import numpy as np
import pandas as pd


def gap_analysis(args):
    """Create a GAP analysis of traits vs taxon."""
    sql = """
        SELECT taxon, level, trait, count(*) AS n
          FROM taxa
     LEFT JOIN traits USING (taxon)
      GROUP BY taxon, level, trait;
    """
    df = pd.read_sql(sql, sqlite3.connect(str(args.sqlite3)))
    df = df.pivot(index=["taxon", "level"], columns="trait", values="n")
    df = df.fillna("")
    df = df.rename(columns={np.nan: "no_traits"})
    df.to_csv(args.csv_file)


def parse_args():
    """Process command-line arguments."""
    description = """Create a GAP analysis of traits vs taxa."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--sqlite3", "-S", required=True, help="""Use this sqlite3 database as input."""
    )

    arg_parser.add_argument(
        "--csv-file",
        "-C",
        type=argparse.FileType("w"),
        required=True,
        help="""Output the results to this CSV file.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    gap_analysis(ARGS)
