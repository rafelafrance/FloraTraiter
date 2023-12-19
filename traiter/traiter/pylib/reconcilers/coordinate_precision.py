from typing import Any

from .base import Base


class CoordinatePrecision(Base):
    label = "dwc:coordinatePrecision"
    aliases = Base.get_aliases(label)

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        if o_val := cls.search(other, cls.aliases):
            return {cls.label: o_val}
        return {}
