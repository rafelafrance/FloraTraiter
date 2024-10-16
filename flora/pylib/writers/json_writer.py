import json
from pathlib import Path

from traiter.pylib.darwin_core import DarwinCore

from flora.pylib.treatments import Treatments


def write_json(treatments: Treatments, json_dir: Path) -> None:
    json_dir.mkdir(parents=True, exist_ok=True)

    for treatment in treatments:
        dwc = DarwinCore()
        _ = [t.to_dwc(dwc) for t in treatment.traits]

        path = json_dir / f"{treatment.path.stem}.json"
        with path.open("w") as f:
            output = dwc.to_dict()
            output["text"] = treatment.text
            json.dump(output, f, indent=4)
