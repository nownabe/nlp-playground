"""Test script."""

import datasets.livedoor_news as ln

from preprocessor import cleaner
from preprocessor import normalizer
from preprocessor import segmenter

from JapaneseTokenizer import MecabWrapper

cleaner = cleaner.Basic()
normalizer = normalizer.Basic()
segmenter = segmenter.Basic()

# nothing = ln.load("data", parse=True)
corpus = ln.load("data",
                 parse=True,
                 cleaner=cleaner,
                 normalizer=normalizer,
                 segmenter=segmenter,
                 limit=100,
                 )

mecab = MecabWrapper(dictType="neologd")

for i in range(10):
    for cat in corpus.categories:
        article = corpus.articles[cat][i]
        print("Title: " + article.title + "\n")

        for sentence in article.content:
            tokenized_sentence = mecab.tokenize(sentence=sentence)

            print("[", end="")
            for token in tokenized_sentence.tokenized_objects:
                print(f"{token.word_surface}:{token.word_stem}:{token.tuple_pos}", end=", ")

            print("]")

        print("\n================================")
        input("Continue to enter any key.")


"""
for cat in corpus.categories:
    for i in range(10):
        print("\n<<<No Preprocess>>>")
        print("Title: " + nothing.articles[cat][i].title + "\n")
        print("\n".join(nothing.articles[cat][i].content))

        print("\n<<<Preprocessed>>>")
        print("Title: " + corpus.articles[cat][i].title + "\n")
        print("\n".join(corpus.articles[cat][i].content))

        print("\n================================")

        input("Continue to enter any key.")
"""
