from collections import namedtuple
from typing import Any

from traiter.traiter.pylib.reconcilers.base import Base

Label = namedtuple("Label", "label match")


class TaxonName(Base):
    sci_name_lb = "dwc:scientificName"

    # kingdom_lb = "dwc:kingdom"
    # phylum_lb = "dwc:phylum"
    # class_lb = "dwc:class"
    # order_lb = "dwc:order"
    family_lb = "dwc:family"
    # subfamily_lb = "dwc:subfamily"
    # tribe_lb = "dwc:tribe"
    # subtribe_lb = "dwc:subtribe"
    # genus_lb = "dwc:genus"
    # subgenus_lb = "dwc:subgenus"
    # infra_genus_lb = "dwc:infragenericEpithet"
    # species_lb = "dwc:specificEpithet"
    # infra_species_lb = "dwc:infraspecificEpithet"
    # cultivar_lb = "dwc:cultivarEpithet"

    matches = [
        Label(
            sci_name_lb,
            Base.get_aliases(
                sci_name_lb,
                """ dwc:suggestedScientificName
            dwc:verbatimScientificName dwc:acceptedScientificName""",
            ),
        ),
        # Label(kingdom_lb, Base.get_aliases(kingdom_lb)),
        # Label(phylum_lb, Base.get_aliases(phylum_lb)),
        # Label(class_lb, Base.get_aliases(class_lb)),
        # Label(order_lb, Base.get_aliases(order_lb)),
        Label(family_lb, Base.get_aliases(family_lb)),
        # Label(subfamily_lb, Base.get_aliases(subfamily_lb)),
        # Label(tribe_lb, Base.get_aliases(tribe_lb)),
        # Label(subtribe_lb, Base.get_aliases(subtribe_lb)),
        # Label(genus_lb, Base.get_aliases(genus_lb)),
        # Label(subgenus_lb, Base.get_aliases(subgenus_lb)),
        # Label(
        #     infra_genus_lb,
        #     Base.get_aliases(
        #         infra_genus_lb,
        #         """
        #     dwc:section dwc:subsection dwc:series dwc:subseries""",
        #     ),
        # ),
        # Label(species_lb, Base.get_aliases(species_lb, "dwc:species")),
        # Label(
        #     infra_species_lb,
        #     Base.get_aliases(
        #         infra_species_lb,
        #         """
        #     dwc:infraSpecificEpithet dwc:intraspecificEpithet dwc:subspecies
        #     dwc:subspeciesName dwc:variety dwc:subvariety dwc:form dwc:subform""",
        #     ),
        # ),
        # Label(cultivar_lb, Base.get_aliases(cultivar_lb)),
    ]

    @classmethod
    def reconcile(
        cls, traiter: dict[str, Any], other: dict[str, Any], text: str
    ) -> dict[str, Any]:
        obj = {}

        for lb, aliases in cls.matches:
            if o_val := cls.search(other, aliases):
                obj[lb] = o_val
            elif t_val := traiter.get(lb):
                obj[lb] = t_val

        return obj
