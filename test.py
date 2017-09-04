"""Test script."""

import random

import datasets.livedoor_news as ln

from preprocessor import cleaner
from preprocessor import normalizer
from preprocessor import segmenter
from preprocessor import stopword_remover

from JapaneseTokenizer import MecabWrapper

from gensim import corpora
from gensim import matutils
from gensim.models import LsiModel

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

import numpy as np

cleaner = cleaner.Basic()
normalizer = normalizer.Basic()
segmenter = segmenter.Basic()

# nothing = ln.load("data", parse=True)
corpus = ln.load("data",
                 parse=True,
                 cleaner=cleaner,
                 normalizer=normalizer,
                 segmenter=segmenter,
                 )

mecab = MecabWrapper(dictType="neologd")

docs = {}
doc_words = []

for cat in corpus.categories:
    docs[cat] = []
    for article in corpus.articles[cat]:
        doc = []

        for sentence in article.content:
            tokenized_sentence = mecab.tokenize(sentence=sentence)

            for token in tokenized_sentence.tokenized_objects:
                doc.append(token.word_stem)

        docs[cat].append(doc)
        doc_words.append(doc)


dictionary = corpora.Dictionary(doc_words)
print(dictionary)
# print(dictionary.token2id)

unfiltered = dictionary.token2id.keys()

dictionary.filter_extremes(no_below=2, no_above=0.5)
filtered = dictionary.token2id.keys()

# print(dictionary)
# print("Filtered: ", end="")
# print(set(unfiltered) - set(filtered))


doc_bows = {}
flat_bows = []

for cat, articles in docs.items():
    doc_bows[cat] = []
    for a in articles:
        bow = dictionary.doc2bow(a)
        # v = list(matutils.corpus2dense([bow], num_terms=len(dictionary)).T[0])
        doc_bows[cat].append(bow)
        flat_bows.append(bow)

print(len(doc_bows))
print(len(flat_bows))

num_topics = 200

lsi_model = LsiModel(flat_bows, num_topics=num_topics)

lsi_docs = []

for cat, docs in doc_bows.items():
    for doc in docs:
        lsi_docs.append((cat, lsi_model[doc]))

random.shuffle(lsi_docs)

# print(doc_bows[corpus.categories[0]][0])
# print(lsi_docs[corpus.categories[0]][0])


def vec2dense(vec, num_terms):
    return list(matutils.corpus2dense([vec], num_terms=num_terms).T[0])

data_all = []
label_all = []

for cat, doc in lsi_docs:
    label_all.append(corpus.categories.index(cat))
    data_all.append(vec2dense(doc, num_topics))

# print(len(data_all))
# print(len(label_all))

# print(data_all[0])
# print(label_all[0])

train_data, test_data, train_label, test_label = train_test_split(data_all, label_all, test_size=0.2)

pipeline = Pipeline([
    ("standard_scaler", StandardScaler()),
    ("svm", SVC())
])

params = {
    "svm__C": np.logspace(0, 2, 5),
    "svm__gamma": np.logspace(-3, 0, 5),
}

clf = GridSearchCV(pipeline, params)
clf.fit(train_data, train_label)

pred = clf.predict(test_data)

print(classification_report(test_label, pred))
print(confusion_matrix(test_label, pred))



"""
for i in range(10):
    for cat in corpus.categories:
        article = corpus.articles[cat][i]
        print("Title: " + article.title + "\n")

        for sentence in article.content:
            tokenized_sentence = mecab.tokenize(sentence=sentence)

            print("Normal  :", end="")
            for token in tokenized_sentence.tokenized_objects:
                print(f"{token.word_surface}", end=" ")

            print("")

            print("Removed1:", end="")
            removed = remover1.remove(tokenized_sentence)
            for token in removed.tokenized_objects:
                print(f"{token.word_surface}", end=" ")

            print("")

            print("Removed2:", end="")
            removed = remover2.remove(tokenized_sentence)
            for token in removed.tokenized_objects:
                print(f"{token.word_surface}", end=" ")

            print("")

        print("\n================================")
        input("Continue to enter any key.")
"""

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
