from typing import Any

from .base import Base


class DecimalLatitude(Base):
    label = "dwc:decimalLatitude"
    aliases = Base.get_aliases(label, "dwc:latitude dwc:verbatimLatitude")

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        if o_val := cls.search(other, cls.aliases):
            return {cls.label: o_val}
        return {}
