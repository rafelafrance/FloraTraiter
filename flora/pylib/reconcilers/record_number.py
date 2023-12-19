from typing import Any

from traiter.traiter.pylib.darwin_core import SEP
from traiter.traiter.pylib.reconcilers.base import Base


class RecordNumber(Base):
    label = "dwc:recordNumber"
    aliases = Base.get_aliases(label, "dwc:record dwc:recordId dwc:recordedNumber")

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        # Default to the GPT version
        if val := cls.search(other, cls.aliases):
            return {cls.label: val}

        vals = traiter.get(cls.label)

        # Handle case where it's missing in both
        if not vals:
            return {}

        # Split the values and take the last one
        # The record number is most often at the end of the label
        vals = vals.split(SEP)

        longest = max(len(v) for v in vals)
        threshold = 2 if longest > 2 else 1

        vals = [v for v in vals if len(v) > threshold]

        return {cls.label: vals[-1]} if vals else {}
