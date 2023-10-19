import re
from abc import ABC, abstractmethod

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
    def calculate(cls, texts: list[str], **kwargs) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
        kws: list[Keyword] = Keyword.load_keywords()

        # calculate ratio for all texts and ratio by each text
        count_all: dict[str, float] = {kw.keyword: 0 for kw in kws}
        count_by_text: list[dict[str, float]] = [{kw.keyword: 0 for kw in kws} for _ in range(len(texts))]
        count_total = 0
        for idx, text in enumerate(tqdm(texts, leave=False, desc="calculating")):
            count_total_by_text = 0
            for keyword in kws:
                ptn = keyword.get_keyword_ptn()
                _text = text.replace(".", ". \n")
                count = len(ptn.findall(_text.lower()))

                # total
                count_all[keyword.keyword] += count
                count_total += count

                # by text
                count_by_text[idx][keyword.keyword] += count
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
