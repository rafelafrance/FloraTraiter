from typing import Any

from traiter.pylib.darwin_core import SEP
from traiter.pylib.reconcilers.base import Base


class RecordNumber(Base):
    label = "dwc:recordNumber"
    aliases = Base.get_aliases(label, "dwc:record dwc:recordId dwc:recordedNumber")

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any]
    ) -> dict[str, str]:
        # Default to the GPT version
        if val := cls.search(other, cls.aliases):
            return {cls.label: val}

        val = traiter.get(cls.label)

        # Handle case where it's missing in both
        if not val:
            return {}

        # Split the values and take the last one that's reasonable, size-wize
        # The record number is most often at the end of the label
        vals = [v for v in val.split(SEP) if len(v) > 2]

        return {cls.label: vals[-1]} if vals else {}
