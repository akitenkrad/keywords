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
        count_all: dict[str, float] = {}
        count_total = 0
        for keyword in kws:
            ptn = keyword.get_keyword_ptn()
            count_all[keyword.keyword] = 0
            for text in texts:
                _text = text.replace(".", ". \n")
                count_all[keyword.keyword] += len(ptn.findall(_text.lower()))
                count_total += len(ptn.findall(_text.lower()))
        for keyword in kws:
            count_all[keyword.keyword] = count_all[keyword.keyword] / (count_total + 1e-10)

        # calculate ratio for each text
        count_by_text: dict[int, dict[str, float]] = {}
        for idx, text in enumerate(texts):
            _text = text.replace(".", ". \n")
            count_by_text[idx] = {}
            count_total_by_text = 0
            for keyword in kws:
                ptn = keyword.get_keyword_ptn()
                count_by_text[idx][keyword.keyword] = len(ptn.findall(_text.lower()))
                count_total_by_text += len(ptn.findall(_text.lower()))
            for keyword in kws:
                count_by_text[idx][keyword.keyword] = count_by_text[idx][keyword.keyword] / (
                    count_total_by_text + 1e-10
                )

        # calculate specialization factor
        factors = []
        for _, kw_count in count_by_text.items():
            factors.append(
                {keyword.keyword: kw_count[keyword.keyword] / (count_all[keyword.keyword] + 1e-10) for keyword in kws}
            )

        return pd.DataFrame(factors)
