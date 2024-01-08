"""
The algorithms for linking traits to the taxon they describe can get involved. This
reader looks for treatment header for the taxon. A header a given regular expression
pattern. The very next taxon is grabbed as the one to associate with the traits.
"""
import sys
from enum import Enum, auto

import rich

from .mimosa_base_reader import BaseReader


class State(Enum):
    START = auto()
    SEARCH = auto()  # Searching for next treatment taxon
    FOUND = auto()  # Taxon found gather traits
    ERROR = auto()  # Problem finding a taxon


class MarkedReader(BaseReader):
    def __init__(self, args):
        super().__init__(args)
        self.pattern = args.pattern
        self.max_distance = args.taxon_distance

    def read(self):
        taxon = "Unknown"
        state = State.START
        distance = 0
        errors = 0
        seen = set()

        for i, ln in enumerate(self.lines, 1):
            ln = ln.strip()

            distance += 1

            if state == State.SEARCH and distance > self.max_distance:
                state = State.ERROR
                errors += 1
                print_error(f"Could not find a taxon: near line {i}")

            if ln.find(self.pattern) > -1:
                state = State.SEARCH

            if state in (State.ERROR, State.START):
                continue

            doc = self.nlp(ln)
            traits = []

            if ln.find(self.pattern) > -1:
                taxon = "Unknown"
                state = State.SEARCH
                distance = 0

            for ent in doc.ents:
                trait = ent._.trait

                if state == State.SEARCH and trait["trait"] == "taxon":
                    try:
                        maybe = trait["taxon"]

                        if isinstance(maybe, list):
                            msg = f"Taxon is a list '{maybe}' at {i}"
                            raise ValueError(msg)

                        words = maybe.split()

                        if len(words) < 2 or words[0][-1] == ".":
                            msg = f"Taxon has a bad form '{maybe}' at {i}"
                            raise ValueError(msg)

                        if any(w.istitle() for w in words[1:]):
                            msg = f"Taxon is malformed '{maybe}' at {i}"
                            raise ValueError(msg)

                        if maybe in seen:
                            msg = f"Taxon already seen '{maybe}' at {i}"
                            raise ValueError(msg)

                        taxon = maybe
                        state = State.FOUND
                        seen.add(taxon)
                        print(f"{i: 6} {taxon}")

                    except ValueError as err:
                        errors += 1
                        print_error(err)

                elif state == State.FOUND and trait["trait"] != "taxon":
                    trait["taxon"] = taxon
                    self.taxon_traits[taxon].append(trait)

                traits.append(trait)

            self.text_traits.append((ln, traits))

        if errors:
            print_error(f"\nThere were {errors} errors\n")

        return self.finish()


def print_error(msg):
    rich.print(
        f"[bold red]{msg}[/bold red]",
        file=sys.stderr,
    )
