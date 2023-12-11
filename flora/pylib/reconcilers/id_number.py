from typing import Any

from traiter.pylib.reconcilers.base import Base


class IdNumber(Base):
    acc_lb = "dwc:accessionNumber"
    id_lb = "dwc:recordedByID"
    num_lb = "dwc:recordNumber"

    acc_match = Base.get_aliases(acc_lb)
    id_match = Base.get_aliases(id_lb, "dwc:recordedById")
    num_match = Base.get_aliases(
        num_lb,
        """
        dwc:record dwc:recordId dwc:recordedNumber dwc:recordnumber""",
    )

    @classmethod
    def reconcile(cls, _: dict[str, Any], other: dict[str, Any]) -> dict[str, str]:
        obj = {}

        if val := cls.search(other, cls.acc_match):
            obj[cls.acc_lb] = val

        if val := cls.search(other, cls.id_match):
            obj[cls.id_lb] = val

        if val := cls.search(other, cls.num_match):
            obj[cls.num_lb] = val

        return obj
