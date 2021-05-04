"""Custom sentence splitter."""

from typing import Optional

from spacy.language import Language
from spacy.tokens import Doc

from traiter.const import CLOSE, QUOTE

SENTENCE = 'traiter.sentence.v1'

EOS = """ . ? ! … """.split()  # End Of Sentence
PREV_EOS = CLOSE + EOS


@Language.factory(SENTENCE)
class Sentence:
    """Shared sentencizer logic."""

    def __init__(self, nlp: Language, name: str, automatic: Optional[list[str]] = None):
        """Build a custom sentencizer."""
        self.nlp = nlp
        self.name = name
        self.automatic = automatic if automatic else []

    def __call__(self, doc: Doc) -> Doc:
        """Break the text into sentences."""
        for i, token in enumerate(doc[:-1]):
            prev = doc[i - 1] if i > 0 else None
            next_ = doc[i + 1]

            # Some tokens are automatically their own sentence
            if (token.ent_type_ in self.automatic
                    and (not prev or self.is_prev(prev))
                    and self.is_next(next_)):
                next_.is_sent_start = True
                token.is_sent_start = True

            # A period followed by a capital letter (or space, digit or another period)
            elif token.text == '.' and self.is_next(next_):
                next_.is_sent_start = True

            # Quotes preceded by a period
            elif token.text in QUOTE and prev and prev.text in EOS:
                next_.is_sent_start = True

            # Not a sentence break
            else:
                next_.is_sent_start = False

        return doc

    @staticmethod
    def is_space(token):
        """Check if the token is space."""
        return token.text.isspace() or token.pos_ == 'SPACE'

    def is_prev(self, token):
        """See if the previous token is a space or a bracket."""
        return self.is_space(token) or token.text in PREV_EOS

    def is_next(self, token):
        """See if the next token starts with an uppercase is a space or period."""
        return (token.prefix_.isupper() or token.prefix_.isdigit()
                or self.is_space(token) or token.text in EOS)
