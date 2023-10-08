import re
from abc import ABC, abstractmethod

import pandas as pd
from nltk import FreqDist

from keywords.keywords import Keyword, KeywordCategory


class SpecializationFactor(object):
    @classmethod
    def calculate(cls, texts: list[str], **kwargs) -> pd.DataFrame:
        kws: list[Keyword] = Keyword.load_keywords()

        # calculate ratio for all text
        count_all: dict[Keyword, float] = {}
        count_total = 0
        for keyword in kws:
            ptn = re.compile(rf"(^|\s)+{keyword.keyword}($|\s)+")
            count_all[keyword] = 0
            for text in texts:
                count_all[keyword] += len(ptn.findall(text))
                count_total += len(ptn.findall(text))
        for keyword in kws:
            count_all[keyword] = count_all[keyword] / (count_total + 1e-10)

        # calculate ratio for each text
        count_by_text: dict[int, dict[Keyword, float]] = {}
        for idx, text in enumerate(texts):
            count_by_text[idx] = {}
            count_total_by_text = 0
            for keyword in kws:
                ptn = re.compile(rf"(^|\s)+{keyword.keyword}($|\s)+")
                count_by_text[idx][keyword] = len(ptn.findall(text))
                count_total_by_text += len(ptn.findall(text))
            for keyword in kws:
                count_by_text[idx][keyword] = count_by_text[idx][keyword] / (count_total_by_text + 1e-10)

        # calculate specialization factor
        factors = []
        for _, kw_count in count_by_text.items():
            factors.append({keyword.keyword: kw_count[keyword] / (count_all[keyword] + 1e-10) for keyword in kws})

        return pd.DataFrame(factors)
