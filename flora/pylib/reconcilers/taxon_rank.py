from typing import Any

from traiter.traiter.pylib.reconcilers.base import Base


class TaxonRank(Base):
    label = "dwc:taxonRank"
    aliases = Base.get_aliases(label, "dwc:verbatimTaxonRank")

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        o_val = cls.search(other, cls.aliases)
        t_val = traiter.get(cls.label, "")

        if (o_val.casefold() == t_val.casefold()) or (o_val and not t_val):
            return {cls.label: o_val}

        if not o_val and t_val:
            return {cls.label: t_val}

        if o_val != t_val:
            return {cls.label: o_val}

        raise ValueError(f"UNKNOWN error in {cls.label}")
