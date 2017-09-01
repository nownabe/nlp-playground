"""Segmenter."""

import re

from itertools import chain

# TODO(nownabe): 改行を無視して文を継続させる末尾記号
# 例:
#   それについても、
#   「ほげほげ」とはほげさん。


class Basic(object):
    """Basic segmenter."""

    BRACKETS = {
        "(": ")",
        "[": "]",
        "「": "」",
        "【": "】",
    }

    OPEN_BRACKETS = BRACKETS.keys()
    CLOSE_BRACKETS = BRACKETS.values()

    TAIL_SYMBOL_RE = re.compile(r"[。!?]")

    def __init__(self):
        """Init."""
        pass

    def segment(self, text):
        """Segment text."""
        sentences = []

        lines = text.splitlines()

        for i in range(len(lines)):
            if not lines[i] == "":
                sentences.append(self._segment_line(lines[i]))

        return list(chain.from_iterable(sentences))

    def _segment_line(self, line):
        sentences = []

        self.sentence = ""
        self.depth_in_brackets = 0
        self.brackets = []

        for c in list(line):
            if self._is_tail(c):
                sentences.append(self.sentence)
                self.sentence = ""

            self.sentence += c

            if self._is_open(c):
                self._open(c)
            elif self._is_close(c):
                self._close()

        if not self.sentence == "":
            sentences.append(self.sentence)

        return sentences

    def _is_tail(self, char):
        if self.depth_in_brackets != 0:
            return False

        if len(self.sentence) == 0:
            return False

        return self.TAIL_SYMBLE_RE.match(self.sentence[-1]) and \
            not self.TAIL_SYMBOLE_RE.match(char)

    def _is_open(self, char):
        return char in self.OPEN_BRACKETS

    def _open(self, char):
        self.depth_in_brackets += 1
        self.brackets.append(char)

    def _is_close(self, char):
        if self.depth_in_brackets == 0:
            return False
        return self.BRACKETS[self.brackets[-1]] == char

    def _close(self):
        self.depth_in_brackets -= 1
        self.brackets.pop()
