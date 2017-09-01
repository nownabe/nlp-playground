"""Cleaners."""

import re


class Basic(object):
    """Basic cleaner."""

    REPLACE_PATTERNS = [
        (r"^[ \t\r\f\v\u3000]+", re.MULTILINE, ""),
        (r"[ \t\r\f\v\u3000]+$", re.MULTILINE, ""),
        (r"^[・■※]\s*", re.MULTILINE, ""),
        (r"https?://[^\s]+", 0, ""),
        (r"[\-0-9a-zA-Z\.]+@[\-0-9a-zA-Z\.]+", 0, ""),
        (r"@[a-zA-Z][0-9a-zA-Z]*", 0, ""),
    ]

    def __init__(self):
        """Init."""
        self.replace_patterns = \
            [(re.compile(p[0], p[1]), p[2]) for p in self.REPLACE_PATTERNS]

    def clean(self, text):
        """Clean text."""
        cleaned_text = text
        for pat in self.replace_patterns:
            cleaned_text = pat[0].sub(pat[1], cleaned_text)

        return cleaned_text
