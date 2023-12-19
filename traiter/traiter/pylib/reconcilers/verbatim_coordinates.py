from typing import Any

from .base import Base


class VerbatimCoordinates(Base):
    label = "dwc:verbatimCoordinates"
    aliases = Base.get_aliases(label, "dwc:coordinates")

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        if o_val := cls.search(other, cls.aliases):
            return {cls.label: o_val}
        elif t_val := traiter.get(cls.label):
            return {cls.label: t_val}
        return {}
