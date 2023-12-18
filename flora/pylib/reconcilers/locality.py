from typing import Any

from traiter.pylib.darwin_core import SEP
from traiter.pylib.reconcilers.base import Base


class Locality(Base):
    loc_lb = "dwc:verbatimLocality"
    rem_lb = "dwc:locationRemarks"
    loc_match = Base.get_aliases(
        loc_lb,
        """
        dwc:locality dwc:localityDescription dwc:localityDetails
        dwc:Location dc:Location dwc:physicalLocation dwc:specificLocality
        dwc:recordedLocation dwc:specificLocality dwc:exactLocation
        dwc:locationCity dwc:city
        """,
    )
    rem_match = Base.get_aliases(rem_lb, "dwc:localityRemarks dwc:locationNotes")

    sub_match = loc_match + [loc.removeprefix("dwc:") for loc in loc_match]

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, Any]:
        o_locality = cls.search(other, cls.loc_match)
        o_remarks = cls.search(other, cls.rem_match)
        t_locality = traiter.get(cls.loc_lb, "")

        # Merge the traiter localities if they're separated by only whitespace
        text = " ".join(text.split())
        t_parts = t_locality.split(SEP)
        t_parts = " ".join(t_parts)
        if text.find(t_parts) > -1:
            t_locality = t_parts

        obj = {}

        # Get verbatim locality
        locality = ""

        if isinstance(o_locality, dict):
            if o_locality := cls.search(o_locality, cls.sub_match):
                locality = o_locality

            elif t_locality:
                locality = t_locality

        elif o_locality:
            locality = o_locality

        elif t_locality:
            locality = t_locality

        # Extend locality
        if t_locality and locality in t_locality:
            obj[cls.loc_lb] = t_locality
        else:
            obj[cls.loc_lb] = locality

        # Get location remarks
        if o_remarks:
            obj[cls.rem_lb] = o_remarks

        return obj
