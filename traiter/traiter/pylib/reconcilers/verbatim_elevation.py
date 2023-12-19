from typing import Any

from .base import Base


class VerbatimElevation(Base):
    label = "dwc:verbatimElevation"
    aliases = Base.get_aliases(label)

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, Any]:
        if o_val := cls.search(other, cls.aliases):
            return {cls.label: o_val}
        elif t_val := traiter.get(cls.label):
            return {cls.label: t_val}
        return {}
