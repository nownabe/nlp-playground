"""Stop word remover."""

from urllib import request


class Basic(object):
    """Basic stop word remover."""

    STOPWORDS_URL = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"

    def __init__(self, tokenizer):
        """Init."""
        self.tokenizer = tokenizer

        with request.urlopen(self.STOPWORDS_URL) as response:
            body = response.read().decode("utf-8")
            self.stopwords = body.splitlines()

    def remove(self, tokenized_sentence):
        """Returns sentence without stop words"""
        return self.tokenizer.filter(
            parsed_sentence=tokenized_sentence,
            stopwords=self.stopwords,
            )
