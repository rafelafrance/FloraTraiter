import csv
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DYN = "dwc:dynamicProperties"

DWC = "dwc:"
DC = "dc:"

SEP = " | "
FIELD_SEP = " ~ "


def read_dwc_terms():
    core, dublin = {}, {}

    path = Path(__file__).parent / "rules" / "terms" / "dwc_terms.csv"
    with path.open() as f:
        for row in csv.DictReader(f):
            name = row["term_localName"]
            name = name[0].lower() + name[1:]

            if row["iri"].find("dublincore") > -1:
                name = DC + name
                dublin[name] = row

            else:
                name = DWC + name

            core[name] = row

    return core, dublin


CORE, DUBLIN = read_dwc_terms()


@dataclass
class DarwinCore:
    props: dict[str, Any] = field(default_factory=lambda: defaultdict(list))
    dyn_props: dict[str, Any] = field(default_factory=lambda: defaultdict(list))

    def to_dict(self) -> dict:
        out = {}

        for key, values in self.props.items():
            out[key] = self.convert_value_list(key, values)

        if self.dyn_props:
            out[DYN] = {}
            for key, values in self.dyn_props.items():
                out[DYN][key] = self.convert_value_list(key, values)

        return out

    @staticmethod
    def convert_value_list(key, values):
        flat = []
        for value in values:
            if isinstance(value, list):
                flat += value
            else:
                flat.append(value)
        values = flat

        if all(isinstance(v, str) for v in values):
            return SEP.join(values)

        if all(isinstance(f, float) for f in values):
            return values if len(values) > 1 else values[0]

        if all(isinstance(f, int) for f in values):
            return values if len(values) > 1 else values[0]

        if all(isinstance(v, dict) for v in values):
            new_list = []
            for val in values:
                new = FIELD_SEP.join(f"{k}: {v}" for k, v in val.items())
                new_list.append(new)
            return SEP.join(new_list)

        msg = f"Field: {key} has mixed value types: {values=}"
        raise ValueError(msg)

    def add(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            key = key if key.startswith(DWC) else self.ns(key)
            if value is not None and value not in self.props[key]:
                self.props[key].append(value)
        return self

    def add_dyn(self, **kwargs) -> "DarwinCore":
        for key, value in kwargs.items():
            if value is not None and value not in self.dyn_props[key]:
                self.dyn_props[key].append(value)
        return self

    @staticmethod
    def format_dict(value: dict) -> dict:
        return {k: v for k, v in value.items() if v is not None}

    @staticmethod
    def ns(name):
        namespace = DC if name in DUBLIN else DWC
        return name if name.startswith(namespace) else namespace + name

    def items(self):
        yield from {k: v for k, v in self.props.items() if k != DYN}.items()
        if self.props[DYN]:
            yield from self.props[DYN].items()

    @staticmethod
    def key(*args, prepend: str | None = None) -> str:
        key = [prepend] if prepend else []
        key += list(args)
        key = " ".join(key).replace("-", " ").split()
        key = [k.title() for k in key]
        key[0] = key[0].lower()
        return "".join(key)
