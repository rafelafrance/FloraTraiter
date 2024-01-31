from dataclasses import dataclass, field
from pathlib import Path

from traiter.pylib import util as t_util
from traiter.pylib.rules.base import Base

from .rules.linkable import Linkable


@dataclass
class Treatment:
    path: Path
    text: str = ""
    traits: list[Base | Linkable] = field(default_factory=list)
    formatted_text: str = ""
    formatted_traits: list[str] = field(default_factory=list)

    def parse(self, nlp):
        with self.path.open() as f:
            self.text = f.read()
            self.text = t_util.compress(self.text)

        doc = nlp(self.text)
        self.traits = [e._.trait for e in doc.ents]
