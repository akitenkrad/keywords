import re
from abc import ABC, abstractmethod
from re import Pattern

import numpy as np
import pandas as pd
from nltk import FreqDist

from keywords.keywords import Keyword, KeywordCategory
from keywords.utils import is_notebook

if is_notebook():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm


class SpecializationFactor(object):
    @classmethod
    def calculate(
        cls, texts: list[str], remove_stopwords: bool = False, **kwargs
    ) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
        kws: list[tuple[str, Pattern]] = []
        for keyword in Keyword.load_keywords():
            if remove_stopwords and keyword.score <= 1:
                continue
            kws.append((keyword.keyword, keyword.get_keyword_ptn()))
        sorted(list(set(kws)), key=lambda x: x[0])

        # calculate ratio for all texts and ratio by each text
        count_all: dict[str, float] = {kw[0]: 0 for kw in kws}
        count_by_text: list[dict[str, float]] = [{kw[0]: 0 for kw in kws} for _ in range(len(texts))]
        count_total = 0
        for idx, text in enumerate(tqdm(texts, leave=False, desc="calculating")):
            count_total_by_text = 0
            for kw, ptn in kws:
                _text = text.replace(".", ". \n")
                count = len(ptn.findall(_text.lower()))

                # total
                count_all[kw] += count
                count_total += count

                # by text
                count_by_text[idx][kw] += count
                count_total_by_text += count

            for kw in count_by_text[idx]:
                count_by_text[idx][kw] /= count_total_by_text + 1e-10

        for kw in count_all.keys():
            count_all[kw] /= count_total + 1e-10

        # calculate specialization factor
        factors = []
        for kw_count in count_by_text:
            factors.append({kw: kw_count[kw] / (count_all[kw] + 1e-10) for kw in count_all})

        return pd.DataFrame(factors)


class TfIdf(object):
    @classmethod
    def calculate(
        cls, texts: list[str], remove_stopwords: bool = False, **kwargs
    ) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
        kws: list[tuple[str, Pattern]] = []
        for keyword in Keyword.load_keywords():
            if remove_stopwords and keyword.score <= 1:
                continue
            kws.append((keyword.keyword, keyword.get_keyword_ptn()))
        sorted(list(set(kws)), key=lambda x: x[0])

        # calculate ratio for all texts and ratio by each text
        tf: list[dict[str, float]] = [{kw[0]: 0 for kw in kws} for _ in range(len(texts))]
        idf: dict[str, float] = {kw[0]: 0 for kw in kws}
        total_word_count = 0
        for idx, text in enumerate(tqdm(texts, leave=False, desc="calculating")):
            for kw, ptn in kws:
                _text = text.replace(".", ". \n")
                count = len(ptn.findall(_text.lower()))

                # TF
                tf[idx][kw] += count
                total_word_count += count

                # IDF
                idf[kw] += 1 if count > 0 else 0

        for kw in idf:
            idf[kw] = np.log(len(texts) / (idf[kw] + 1e-10)) + 1

        for kw_count in tf:
            for kw, value in kw_count.items():
                kw_count[kw] = value / (total_word_count + 1e-10)

        tfidf: list[dict[str, float]] = [{kw[0]: 0 for kw in kws} for _ in range(len(texts))]
        for idx in range(len(texts)):
            for kw, _ in kws:
                tfidf[idx][kw] = tf[idx][kw] * idf[kw]

        return pd.DataFrame(tfidf)
