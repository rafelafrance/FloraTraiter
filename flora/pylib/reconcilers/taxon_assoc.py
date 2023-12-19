import re
from typing import Any

from traiter.traiter.pylib.darwin_core import SEP
from traiter.traiter.pylib.reconcilers.base import Base


class TaxonAssociation(Base):
    label = "dwc:associatedTaxa"
    aliases = Base.get_aliases(
        label,
        """
        dwc:associatedSpecies dwc:additionalSpecies dwc:associatedFlora
        dwc:Associates""",
    )

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        t_val = traiter.get(cls.label, "")
        t_vals = [v for v in t_val.split(SEP) if v]
        t_val = t_val.casefold()

        o_val = cls.search(other, cls.aliases)
        o_vals = []
        match o_val:
            case str():
                o_vals = re.split(r"\s*[,;|]\s*", o_val)
            case list():
                o_vals = [v[0] if isinstance(v, list) else v for v in o_val]

        for o_val in o_vals:
            if o_val and o_val.casefold() not in t_val:
                t_vals.append(o_val)

        vals = {cls.label: SEP.join(t_vals)} if t_vals else {}

        return vals
