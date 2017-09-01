"""Test script."""

import datasets.livedoor_news as ln

from preprocessor import cleaner

cleaner = cleaner.Basic()

nothing = ln.load("data", parse=True)
corpus = ln.load("data", parse=True, cleaner=cleaner)

for cat in corpus.categories:
    for i in range(10):
        # print("\n<Title>")
        # print(a.title)
        # print("\n<Category>")
        # print(a.category)
        # print("\n<Timestamp>")
        # print(a.timestamp)
        # print("\n<URL>")
        # print(a.url)

        print("\n<<<No Preprocess>>>")
        print("Title: " + nothing.articles[cat][i].title + "\n")
        print("\n".join(nothing.articles[cat][i].content))

        print("\n<<<Preprocessed>>>")
        print("Title: " + corpus.articles[cat][i].title + "\n")
        print("\n".join(corpus.articles[cat][i].content))

        print("\n================================")

        input("Continue to enter any key.")
