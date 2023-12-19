from typing import Any

from traiter.traiter.pylib.reconcilers.base import Base


class IdNumber(Base):
    acc_lb = "dwc:accessionNumber"
    id_lb = "dwc:recordedByID"

    acc_match = Base.get_aliases(acc_lb)
    id_match = Base.get_aliases(id_lb, "dwc:recordedById")

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        obj = {}

        if val := cls.search(other, cls.acc_match):
            obj[cls.acc_lb] = val

        if val := cls.search(other, cls.id_match):
            obj[cls.id_lb] = val

        return obj
