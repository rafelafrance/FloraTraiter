import base64
import io
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import regex as re
from PIL import Image, UnidentifiedImageError
from traiter.pylib import util as t_util
from traiter.pylib.rules.base import Base

from .rules.linkable import Linkable

MAX_SIZE = 600.0  # pixels


@dataclass
class Label:
    path: Path
    text: str = ""
    traits: list[Base | Linkable] = field(default_factory=list)
    image_path: Path | None = None
    encoded_image: str = ""
    word_count: int = 0
    valid_words: int = 0
    score: float = 0.0
    formatted_text: str = ""
    formatted_traits: list[str] = field(default_factory=list)

    def parse(self, nlp, image_paths, vocabulary):
        with open(self.path) as f:
            self.text = f.read()
            self.text = t_util.compress(self.text)

        doc = nlp(self.text)
        self.traits = [e._.trait for e in doc.ents]

        self.image_path = image_paths.get(self.path.stem)
        self.encoded_image = self.encode_image()

        self.score_label(vocabulary)

    def score_label(self, vocabulary):
        """
        Score the label content.

        score = number of words in the label (words = all chars are letters)
                divided by the number of those words in the vocabulary
        """
        all_words = [t for t in re.split(r"[^\p{L}]+", self.text.lower()) if t]
        self.word_count = len(all_words)

        self.valid_words = sum(1 for w in all_words if w in vocabulary)

        self.score = 0.0
        if self.word_count > 0:
            self.score = round(self.valid_words / self.word_count, 2)

    def encode_image(self) -> str:
        if not self.image_path:
            return ""

        with warnings.catch_warnings():  # Turn off EXIF warnings
            warnings.filterwarnings("ignore", category=UserWarning)
            try:
                image = Image.open(self.image_path)
            except (FileNotFoundError, TypeError, ValueError, UnidentifiedImageError):
                return ""

        if image.size[1] > image.size[0]:
            width = round(MAX_SIZE / image.size[1] * image.size[0])
            image = image.resize((width, int(MAX_SIZE)))
        else:
            height = round(MAX_SIZE / image.size[0] * image.size[1])
            image = image.resize((int(MAX_SIZE), height))

        memory = io.BytesIO()
        image.save(memory, format="JPEG")
        image_bytes = memory.getvalue()

        string = base64.b64encode(image_bytes).decode()
        return string

    def too_short(self, length_cutoff):
        return self.word_count < length_cutoff

    def bad_score(self, score_cutoff):
        return self.score < score_cutoff
