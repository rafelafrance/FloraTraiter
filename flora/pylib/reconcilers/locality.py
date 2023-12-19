from typing import Any

from traiter.traiter.pylib.darwin_core import SEP
from traiter.traiter.pylib.reconcilers.base import Base


class Locality(Base):
    label = "dwc:verbatimLocality"
    loc_match = Base.get_aliases(
        label,
        """
        dwc:locality dwc:localityDescription dwc:localityDetails
        dwc:Location dc:Location dwc:physicalLocation dwc:specificLocality
        dwc:recordedLocation dwc:specificLocality dwc:exactLocation
        dwc:locationCity dwc:city
        """,
    )
    rem_match = Base.get_aliases(
        "dwc:locationRemarks dwc:localityRemarks dwc:locationNotes"
    )

    sub_match = loc_match + [loc.removeprefix("dwc:") for loc in loc_match]

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, Any]:
        o_locality = cls.search(other, cls.loc_match)
        o_remarks = cls.search(other, cls.rem_match)
        t_locality = traiter.get(cls.label, "")

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
            locality = t_locality

        # Get location remarks
        if o_remarks and isinstance(o_remarks, str) and o_remarks not in locality:
            if locality + " " + o_remarks in text:
                locality += " " + o_remarks
            elif o_remarks + " " + locality in text:
                locality = o_remarks + " " + locality
            else:
                locality += locality + SEP + o_remarks

        obj[cls.label] = locality
        return obj
