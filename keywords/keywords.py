from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from pathlib import Path


class KeywordCategory(Enum):
    NLP_TASK = "NLP Task"
    NLP_TOPIC = "NLP Topic"
    NLP_MODEL = "NLP Model"
    ML_TOPIC = "Machine Learning Topic"
    GRAPH_TASK = "Graph Task"
    GRAPH_TOPIC = "Graph Topic"
    GRAPH_MODEL = "Graph Model"
    SECURITY_TOPIC = "Security Topic"
    SECURITY_ATTACK = "Security Attack"

    @classmethod
    def from_str(cls, w: str) -> KeywordCategory:
        kw_map = {k.value: k for k in KeywordCategory}
        return kw_map[w]


@total_ordering
@dataclass(frozen=True)
class Keyword(object):
    category: KeywordCategory
    keyword: str

    def __eq__(self, other):
        assert isinstance(other, Keyword)
        return self.category == other.category and self.keyword == other.keyword

    def __lt__(self, other):
        assert isinstance(other, Keyword)
        return (self.category.name, self.keyword) < (other.category.name, other.keyword)

    @classmethod
    def load_keywords(cls, categories: list[KeywordCategory] = []) -> list[Keyword]:
        keywords = []

        with open(Path(__file__).parent / "rsc" / "ml_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [Keyword(KeywordCategory.from_str(item["category"]), item["keyword"]) for item in json.load(f)]
        with open(Path(__file__).parent / "rsc" / "nlp_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [Keyword(KeywordCategory.from_str(item["category"]), item["keyword"]) for item in json.load(f)]
        with open(Path(__file__).parent / "rsc" / "graph_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [Keyword(KeywordCategory.from_str(item["category"]), item["keyword"]) for item in json.load(f)]

        if len(categories) > 0:
            keywords = [keyword for keyword in keywords if keyword.category in categories]

        keywords = sorted(list(set(keywords)))

        return keywords

    def get_keyword_ptn(self) -> re.Pattern:
        return re.compile(rf"(^|\s)+{self.keyword.lower()}s*($|\s\.)+")
