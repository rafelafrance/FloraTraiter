from typing import Any

from traiter.traiter.pylib.reconcilers.base import Base


class Sex(Base):
    label = "dwc:sex"
    aliases = Base.get_aliases(label, "sex")

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, Any]:
        o_sex = cls.search(other, cls.aliases)
        t_sex = traiter.get(cls.label)

        obj = {}

        if t_sex and o_sex in t_sex:
            return {cls.label: o_sex}

        if o_sex and not t_sex:
            return {cls.label: o_sex}

        if not o_sex and t_sex:
            return {cls.label: t_sex}

        return obj
