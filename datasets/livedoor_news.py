"""Toolset for livedoor news corpus."""

import os
import re

from datetime import datetime


def load(directory, parse=False, cleaner=None, normalizer=None):
    """Load livedoor news corpus."""
    return LivedoorNewsCorpus(directory, parse, cleaner, normalizer)


class LivedoorNewsArticle(object):
    """Livedoor News Article class."""

    def __init__(self,
                 category=None,
                 content=None,
                 timestamp=None,
                 title=None,
                 url=None):
        """init."""
        self.category = category
        self.content = content
        self.timestamp = timestamp
        self.title = title
        self.url = url


class LivedoorNewsParser(object):
    """Parser for livedoor news corpus."""

    def __init__(self, cleaner=None, normalizer=None, segmenter=None):
        """init."""
        self.cleaner = cleaner
        self.normalizer = normalizer
        self.segmenter = segmenter

    def parse(self, text, category=None):
        """Parse raw corpus into LivedoorNewsArticle object."""
        lines = text.splitlines()
        url = lines[0]
        timestamp = datetime.strptime(lines[1], "%Y-%m-%dT%H:%M:%S%z")
        title = self._preprocess(lines[2])
        content = self._segment(self._preprocess("\n".join(lines[3:])))

        return LivedoorNewsArticle(
            category=category,
            content=content,
            timestamp=timestamp,
            title=title,
            url=url
        )

    def _preprocess(self, text):
        result = text

        if self.cleaner:
            result = self.cleaner.clean(result)

        if self.normalizer:
            result = self.normalizer.normalize(result)

        return result

    def _segment(self, content):
        if self.segmenter:
            return self.segmenter.segment(content)
        else:
            return content.splitlines()


class LivedoorNewsCorpus(object):
    """Livedoor News Corpus class."""

    DIRECTORY_PREFIX = "livedoor_news/text"
    IGNORE_RE = re.compile("LICENSE")

    def __init__(self, directory, parse=False, cleaner=None, normalizer=None):
        """init."""
        self.directory = directory
        self.parse = parse
        self.cleaner = cleaner
        self.normalizer = normalizer

        self.base_path = os.path.join(directory, self.DIRECTORY_PREFIX)
        self.categories = self._get_categories()
        self.raw_data = {}
        for c in self.categories:
            self._load_category(c)

        if parse:
            self._parse_corpus()

    def _get_categories(self):
        categories = []
        for c in os.listdir(self.base_path):
            if os.path.isdir(os.path.join(self.base_path, c)):
                categories.append(c)

        return categories

    def _load_category(self, category):
        self.raw_data[category] = []
        path = os.path.join(self.base_path, category)
        for file in os.listdir(path):
            if not self.IGNORE_RE.match(file):
                with open(os.path.join(path, file)) as f:
                    self.raw_data[category].append(f.read())

    def _parse_corpus(self):
        self.articles = {}
        parser = LivedoorNewsParser(
            cleaner=self.cleaner,
            normalizer=self.normalizer
        )

        for c in self.categories:
            self.articles[c] = []

            for data in self.raw_data[c]:
                self.articles[c].append(parser.parse(data, category=c))
