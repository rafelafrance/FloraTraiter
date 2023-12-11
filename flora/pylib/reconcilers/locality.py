from typing import Any

from traiter.pylib.reconcilers.base import Base


class Locality(Base):
    loc_lb = "dwc:verbatimLocality"
    rem_lb = "dwc:locationRemarks"
    loc_match = Base.get_aliases(
        loc_lb,
        """
        dwc:locality dwc:localityDescription dwc:localityDetails dwc:localityRemarks
        dwc:Location dc:Location dwc:locationCity dwc:physicalLocation dwc:city
        dwc:recordedLocation dwc:specificLocality dwc:exactLocation
        """,
    )
    rem_match = Base.get_aliases(rem_lb, "dwc:locationNotes")

    @classmethod
    def reconcile(cls, _: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
        o_loc = cls.search(other, cls.loc_match)
        o_rem = cls.search(other, cls.rem_match)

        obj = {}

        # Just use whatever is in the OpenAI output
        if o_loc:
            obj[cls.loc_lb] = o_loc

        if o_rem:
            obj[cls.rem_lb] = o_rem

        return obj
