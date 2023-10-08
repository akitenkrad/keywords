from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class KeywordCategory(Enum):
    NLP_TASK = "NLP Task"
    NLP_TOPIC = "NLP Topic"
    NLP_MODEL = "NLP Model"
    ML_TOPIC = "Machine Learning Topic"
    GRAPH_TASK = "Graph Task"
    GRAPH_TOPIC = "Graph Topic"
    GRAPH_MODEL = "Graph Model"

    @classmethod
    def from_str(cls, w: str) -> KeywordCategory:
        kw_map = {k.value: k for k in KeywordCategory}
        return kw_map[w]


@dataclass(frozen=True)
class Keyword(object):
    category: str
    keyword: KeywordCategory

    @classmethod
    def load_keywords(cls) -> list[Keyword]:
        keywords = []
        with open(Path(__file__).parent / "rsc" / "ml_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [Keyword(item["keyword"], KeywordCategory.from_str(item["category"])) for item in json.load(f)]
        with open(Path(__file__).parent / "rsc" / "nlp_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [Keyword(item["keyword"], KeywordCategory.from_str(item["category"])) for item in json.load(f)]
        with open(Path(__file__).parent / "rsc" / "graph_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [Keyword(item["keyword"], KeywordCategory.from_str(item["category"])) for item in json.load(f)]
        return keywords
