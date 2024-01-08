import re
from calendar import IllegalMonthError
from dataclasses import dataclass
from datetime import date as dt
from pathlib import Path
from typing import ClassVar

from dateutil import parser
from dateutil.relativedelta import relativedelta
from spacy.language import Language
from spacy.util import registry

from traiter.pylib import term_util
from traiter.pylib.darwin_core import DarwinCore
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match

from .base import Base


@dataclass(eq=False)
class Date(Base):
    # Class vars ----------
    date_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "date_terms.csv"
    month_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "month_terms.csv"
    numeric_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "numeric_terms.csv"
    all_csvs: ClassVar[list[Path]] = [date_csv, month_csv, numeric_csv]
    sep: ClassVar[str] = "(.,;/_'-"
    replace: ClassVar[dict[str, str]] = term_util.term_data(all_csvs, "replace")
    # ---------------------

    date: str = None
    century_adjust: bool = None
    missing_day: bool = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add(
            eventDate=self.date,
            verbatimEventDate=self._text,
        )

    @property
    def key(self):
        return DarwinCore.ns("eventDate")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="date_terms", path=cls.all_csvs)
        add.trait_pipe(nlp, name="date_patterns", compiler=cls.date_patterns())
        add.cleanup_pipe(nlp, name="date_cleanup")

    @classmethod
    def date_patterns(cls):
        decoder = {
            "-": {"TEXT": {"REGEX": rf"^[{cls.sep}]$"}},
            "/": {"TEXT": {"REGEX": r"^/$"}},
            "99": {"TEXT": {"REGEX": r"^\d\d?$"}},
            "99-99": {"TEXT": {"REGEX": rf"^\d\d?[{cls.sep}]+\d\d$"}},
            "99-9999": {"TEXT": {"REGEX": rf"^\d\d?[{cls.sep}]+[12]\d\d\d$"}},
            "9999": {"TEXT": {"REGEX": r"^[12]\d\d\d$"}},
            ":": {"TEXT": {"REGEX": r"^[:=]+$"}},
            "label": {"ENT_TYPE": "date_label"},
            "month": {"ENT_TYPE": "month"},
            "roman": {"ENT_TYPE": "roman"},
        }
        return [
            Compiler(
                label="date",
                on_match="date_match",
                keep="date",
                decoder=decoder,
                patterns=[
                    "label? :? 99     -* month -* 99",
                    "label? :? 99     -* month -* 9999",
                    "label? :? 9999   -* month -* 99",
                    "label  :? 99     -* roman -* 99",
                    "label? :? 99     -* roman -* 9999",
                    "label? :? 9999   -* roman -* 99",
                    "label? :? 99     -  99    -  99",
                    "label? :? 99     -  99    -  9999",
                    "label? :? month+ -* 99    -* 9999",
                    "label? :? 9999   -  99    -  99",
                    "label? :? month+ -* 99-9999",
                    "label? :? month+ -* 99-99",
                ],
            ),
            Compiler(
                label="short_date",
                id="date",
                on_match="short_date_match",
                keep="date",
                decoder=decoder,
                patterns=[
                    "label? :? 9999   -* month",
                    "label? :? month+ -* 9999",
                    "label? :? 99-9999",
                    "label? :? 99 / 9999",
                ],
            ),
        ]

    @classmethod
    def date_match(cls, ent):
        frags = []
        century_adjust = None

        for token in ent:
            # Get the numeric parts
            if re.match(rf"^[\d{cls.sep}]+$", token.text):
                parts = [p for p in re.split(rf"[{cls.sep}]+", token.text) if p]
                if parts:
                    frags += parts

            # Get a month name
            elif token._.term in ("month", "roman"):
                month = cls.replace.get(
                    token.text,
                    cls.replace.get(token.lower_, token.lower_),
                )
                frags.append(month)

        # Try to parse the date
        text = " ".join(frags)
        try:
            date_ = parser.parse(text).date()
        except (parser.ParserError, IllegalMonthError):
            raise reject_match.RejectMatch from None

        # Handle missing centuries like: May 22, 08
        if date_ > dt.today():
            date_ -= relativedelta(years=100)
            century_adjust = True

        if date_ > dt.today():
            raise reject_match.RejectMatch

        date_ = date_.isoformat()[:10]

        return super().from_ent(
            ent,
            date=date_,
            century_adjust=century_adjust,
            missing_day=None,
        )

    @classmethod
    def short_date(cls, ent):
        date_ = Date.date_match(ent)
        date_.trait = "date"
        date_.missing_day = True
        date_.date = date_.date[:7]
        return date_


@registry.misc("date_match")
def date_match(ent):
    return Date.date_match(ent)


@registry.misc("short_date_match")
def short_date_match(ent):
    return Date.short_date(ent)
