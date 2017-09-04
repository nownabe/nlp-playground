"""Stop word remover."""

from urllib import request


class Basic(object):
    """Basic stop word remover."""

    STOPWORDS_URL = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"
    DEFAULT_POS = [("名詞", ), ("動詞", ), ("形容詞", ), ("副詞", )]

    def __init__(self, dic=True, pos=False):
        """Init."""
        self.dic = dic

        if pos and not isinstance(pos, list):
            self.pos = self.DEFAULT_POS
        else:
            self.pos = pos

        with request.urlopen(self.STOPWORDS_URL) as response:
            body = response.read().decode("utf-8")
            self.stopwords = body.splitlines()

    def remove(self, tokenized_sentence):
        """Returns sentence without stop words"""

        filtered = tokenized_sentence

        if self.dic:
            filtered = filtered.filter(stopwords=self.stopwords)

        if self.pos:
            filtered = filtered.filter(pos_condition=self.pos)

        return filtered
