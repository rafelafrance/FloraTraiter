from typing import Any

from traiter.traiter.pylib.reconcilers.base import Base


class TaxonAuthority(Base):
    label = "dwc:scientificNameAuthorship"
    aliases = Base.get_aliases(
        label,
        """
        dwc:scientificNameAuth dwc:scientificNameAuthor dwc:sciname_author
        """,
    )

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, str]:
        if o_val := cls.search(other, cls.aliases):
            return {cls.label: o_val}
        elif t_val := traiter.get(cls.label):
            return {cls.label: t_val}
        return {}
