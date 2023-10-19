from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from pathlib import Path
from typing import Any


class KeywordCategory(Enum):
    NLP_TASK = "NLP Task"
    NLP_TOPIC = "NLP Topic"
    NLP_MODEL = "NLP Model"
    CV_TASK = "CV Task"
    CV_TOPIC = "CV Topic"
    CV_MODEL = "CV Model"
    ML_TOPIC = "Machine Learning Topic"
    GRAPH_TASK = "Graph Task"
    GRAPH_TOPIC = "Graph Topic"
    GRAPH_MODEL = "Graph Model"
    SECURITY_TOPIC = "Security Topic"
    SECURITY_ATTACK = "Security Attack"
    SECURITY_TASK = "Security Task"

    @classmethod
    def from_str(cls, w: str) -> KeywordCategory:
        kw_map = {k.value: k for k in KeywordCategory}
        return kw_map[w]


@total_ordering
@dataclass(frozen=True)
class Keyword(object):
    category: KeywordCategory
    word: str
    alias: str
    use_alias: bool

    def __eq__(self, other):
        assert isinstance(other, Keyword)
        return self.category == other.category and self.word == other.word

    def __lt__(self, other):
        assert isinstance(other, Keyword)
        return (self.category.name, self.keyword) < (other.category.name, other.keyword)

    @property
    def keyword(self):
        if self.use_alias:
            return self.alias
        else:
            return self.word

    @classmethod
    def load_keywords(cls, categories: list[KeywordCategory] = []) -> list[Keyword]:
        keywords = []

        with open(Path(__file__).parent / "rsc" / "ml_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True)
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "nlp_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True)
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "graph_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True)
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "security_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True)
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "cv_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True)
                for item in json.load(f)
            ]

        if len(categories) > 0:
            keywords = [keyword for keyword in keywords if keyword.category in categories]

        keywords = sorted(list(set(keywords)))

        return keywords

    def get_keyword_ptn(self) -> re.Pattern:
        _keyword = self.keyword.lower().replace("-", r"(\-|\s)*").replace(" ", r"(\s|\-)*")
        return re.compile(
            rf"(?P<PREK>(^|\s|\()+)(?P<KEYWORD>{_keyword}(s|ing|al|d|ed|\-[^\s]+)*)(?P<POSTK>($|\s|\.|,|:|;|\))+)",
            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category.value,
            "word": self.word,
            "alias": self.alias,
        }
