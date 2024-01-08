"""
Utilities for working with vocabularies.

Based off of symmetric deletes method from SeekStorm. MIT license.
https://seekstorm.com/blog/1000x-spelling-correction/
"""
import logging
import sqlite3
from pathlib import Path

import pandas as pd
import regex as re


class SpellWell:
    def __init__(self, min_freq=100, min_len=3):
        self.min_len = min_len
        self.min_freq = min_freq
        self.cxn = sqlite3.connect(":memory:")
        self.db_to_memory()

    def db_to_memory(self):
        path = Path(__file__).parent / "rules" / "terms"
        df = pd.read_csv(path / "misspellings.zip")
        df = df.loc[df["freq"] >= self.min_freq]
        df = df.loc[df["miss"].str.len() >= self.min_len]
        df.to_sql("spells", self.cxn)

        df = pd.read_csv(path / "vocab.zip")
        df = df.loc[df["freq"] >= self.min_freq]
        df.to_sql("vocab", self.cxn)

        indexes = """
            create index spells_miss on spells (miss);
            create index vocab_word on vocab (word);
            """
        try:
            self.cxn.executescript(indexes)
        except sqlite3.OperationalError:
            logging.exception("Could not create SpellWell database")

    def correct(self, word: str, dist=1) -> str:
        if not word:
            return ""

        if hit := (self.best([word], 0) or self.best([word], 1)):
            return hit

        all_deletes = deletes1(word)
        if dist > 1:
            all_deletes |= deletes2(word)

        if hit := self.best(list(all_deletes), dist):
            return hit

        return word

    def best(self, words, dist: int) -> str:
        q_marks = ", ".join(["?"] * len(words))
        args = [*words, dist]
        sql = f"""select word, dist, freq
                    from spells
                   where miss in ({q_marks})
                     and dist <= ?
                order by freq desc"""  # noqa: S608 hardcoded-sql-expression
        hit = self.cxn.execute(sql, args).fetchone()
        return hit[0] if hit else ""

    @staticmethod
    def is_letters(text: str) -> bool:
        return bool(re.match(r"^\p{L}+$", text))

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """Split the text into words and non-words."""
        return re.split(r"([^\p{L}]+)", text)

    def is_word(self, word: str) -> bool:
        sql = "select word from vocab where word = ?"
        hit = self.cxn.execute(sql, (word,)).fetchone()
        return bool(hit)

    def freq(self, word: str) -> int:
        sql = "select freq from vocab where word = ?"
        hit = self.cxn.execute(sql, (word,)).fetchone()
        return hit[0] if hit else 0

    def vocab_to_set(self) -> set[str]:
        return {r[0] for r in self.cxn.execute("select word from vocab") if r[0]}

    def hits(self, text: str) -> int:
        """
        Count the number of words in the text that are in our corpus.

        A hit is:
        - A direct match in the vocabularies
        - A number like: 99.99
        """
        count = sum(1 for w in self.tokenize(text) if self.is_word(w))
        count += sum(1 for _ in re.findall(r"\d+", text))
        return count


def deletes1(word: str) -> set[str]:
    return {word[:i] + word[i + 1 :] for i in range(len(word))}


def deletes2(word: str) -> set[str]:
    return {d2 for d1 in deletes1(word) for d2 in deletes1(d1)}
