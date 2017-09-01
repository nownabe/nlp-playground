"""Normalizer."""

import re

import neologdn


class Basic(object):
    """Basic normalizer."""

    REPLACE_PATTERNS = [
        (r"&amp;", 0, "&"),
    ]

    def __init__(self):
        """Init."""
        self.replace_patterns = \
            [(re.compile(p[0], p[1]), p[2]) for p in self.REPLACE_PATTERNS]

    def normalize(self, text):
        """Clean text."""
        replaced_text = text

        for pat in self.replace_patterns:
            replaced_text = pat[0].sub(pat[1], replaced_text)

        return neologdn.normalize(replaced_text)
