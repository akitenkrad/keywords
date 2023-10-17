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
            ptn = keyword.get_keyword_ptn()
            count_all[keyword] = 0
            for text in texts:
                count_all[keyword] += len([item for item in ptn.findall(text.lower()) if keyword.keyword in item])
                count_total += len([item for item in ptn.findall(text.lower()) if keyword.keyword in item])
        for keyword in kws:
            count_all[keyword] = count_all[keyword] / (count_total + 1e-10)

        # calculate ratio for each text
        count_by_text: dict[int, dict[Keyword, float]] = {}
        for idx, text in enumerate(texts):
            count_by_text[idx] = {}
            count_total_by_text = 0
            for keyword in kws:
                ptn = keyword.get_keyword_ptn()
                count_by_text[idx][keyword] = len(
                    [item for item in ptn.findall(text.lower()) if keyword.keyword in item]
                )
                count_total_by_text += len([item for item in ptn.findall(text.lower()) if keyword.keyword in item])
            for keyword in kws:
                count_by_text[idx][keyword] = count_by_text[idx][keyword] / (count_total_by_text + 1e-10)

        # calculate specialization factor
        factors = []
        for _, kw_count in count_by_text.items():
            factors.append({keyword.keyword: kw_count[keyword] / (count_all[keyword] + 1e-10) for keyword in kws})

        return pd.DataFrame(factors)
