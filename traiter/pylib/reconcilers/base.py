from pathlib import Path
from typing import Any, Callable

from traiter.pylib import term_util

from ..rules import terms


class Template:
    def __init__(self, *actions):
        self._actions = [a.reconcile for a in actions]

    @property
    def actions(self) -> list[Callable]:
        return self._actions

    def append(self, action):
        self._actions.append(action.reconcile)


class Base:
    nil = "null none not provided not specified".casefold()

    unit_csv = Path(terms.__file__).parent / "unit_length_terms.csv"
    tic_csv = Path(terms.__file__).parent / "unit_tic_terms.csv"
    factors_cm = term_util.term_data((unit_csv, tic_csv), "factor_cm", float)
    factors_m = {k: v / 100.0 for k, v in factors_cm.items()}

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        raise NotImplementedError

    @classmethod
    def search(cls, other: dict[str, Any], aliases: list[str], default: Any = ""):
        for alias in aliases:
            if value := other.get(alias):
                if isinstance(value, str) and value.casefold() in cls.nil:
                    return default
                return value
        return default

    @classmethod
    def wildcard(cls, other, pattern: str, default=""):
        pattern = pattern.casefold()
        for key in other.keys():
            folded = key.casefold()
            if folded in cls.nil:
                return default
            if folded.find(pattern) > -1:
                return other[key]
        return default

    @staticmethod
    def get_aliases(*args) -> list[str]:
        old = " ".join(args).split()
        keys = {}
        for k in old:
            keys[k] = 1
            keys[k.lower()] = 1
        return list(keys.keys())
