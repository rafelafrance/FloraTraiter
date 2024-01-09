from dataclasses import dataclass

import traiter.pylib.darwin_core as t_dwc

ASSOC = "dwc:associatedTaxa"
SEP = t_dwc.SEP


@dataclass
class DarwinCore(t_dwc.DarwinCore):
    def add_assoc(self, **kwargs) -> "DarwinCore":
        if ASSOC not in self.props:
            self.props[ASSOC] = []

        for key, value in kwargs.items():
            if value is not None:
                self.props[ASSOC].append({key: value})

        return self
