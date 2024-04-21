from __future__ import annotations

import csv
import json
import os
import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from glob import glob
from logging import Logger
from pathlib import Path
from typing import Any, Optional

import ipadic
import MeCab
import pykakasi
from argostranslate import package, translate
from IPython.display import HTML
from tqdm import tqdm

TEMP_DICT_CSV = Path("/tmp/tmp_dict.csv")
USER_DIC = "/usr/local/lib/mecab/user.dic"


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
    ICT_TOPIC = "ICT Topic"
    OTHER = "Other"

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
    use_alias: bool = True
    score: float = -1

    def __eq__(self, other):
        assert isinstance(other, Keyword)
        assert self.use_alias == other.use_alias, "Keywords are not comparable"
        if self.use_alias:
            return self.category == other.category and self.alias == other.alias
        else:
            return self.category == other.category and self.word == other.word

    def __lt__(self, other):
        assert isinstance(other, Keyword)
        return (self.category.name, self.keyword) < (other.category.name, other.keyword)

    @classmethod
    def __prepare_argostranslate(cls, from_code: str, to_code: str):
        package.update_package_index()
        available_packages = package.get_available_packages()
        packages_to_install = next(
            filter(lambda x: x.from_code == from_code and x.to_code == to_code, available_packages)
        )
        package.install_from_path(packages_to_install.download())

    @property
    def keyword(self) -> str:
        if self.use_alias:
            return self.alias
        else:
            return self.word

    @classmethod
    def load_keywords(
        cls, categories: list[KeywordCategory] = [], with_translated: str = "", logger: Optional[Logger] = None
    ) -> list[Keyword]:
        if with_translated != "":
            cls.__prepare_argostranslate("en", with_translated)

        keywords = []

        with open(Path(__file__).parent / "rsc" / "ml_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True, item["score"])
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "nlp_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True, item["score"])
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "graph_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True, item["score"])
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "security_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True, item["score"])
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "cv_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True, item["score"])
                for item in json.load(f)
            ]
        with open(Path(__file__).parent / "rsc" / "ict_keywords.json", mode="rt", encoding="utf-8") as f:
            keywords += [
                Keyword(KeywordCategory.from_str(item["category"]), item["word"], item["alias"], True, item["score"])
                for item in json.load(f)
            ]

        if len(categories) > 0:
            keywords = [keyword for keyword in keywords if keyword.category in categories]

        if with_translated != "":
            n_kws = len(keywords)
            for i in tqdm(range(n_kws), desc="Translating keywords", leave=False):
                try:
                    keyword = keywords[i]
                    translated = translate.translate(keyword.word, "en", with_translated)
                    keywords.append(
                        Keyword(keyword.category, translated, keyword.alias, keyword.use_alias, keyword.score)
                    )
                except Exception as e:
                    if logger:
                        logger.error(f"Error translating {keyword.word}: {e}")
                    else:
                        tqdm.write(f"Error translating {keyword.word}: {e}")

        keywords = sorted(list(set(keywords)))

        return keywords

    @classmethod
    def highlight_keywords(cls, text: str, keywords: list[str], color: str = "yellow"):
        highlight_class = {
            "yellow": "highlight-y",
            "green": "highlight-g",
            "blue": "highlight-b",
            "red": "highlight-r",
        }[color]
        html_text = (
            "<style>"
            + ".highlight-y { color: yellow; } "
            + ".highlight-g { color: lightgreen; } "
            + ".highlight-b { color: lightblue; } "
            + ".highlight-r { color: red; } "
            + ".abstract {font-family: CodeM; }"
            + "</style> "
            + os.linesep
            + "<div class='abstract'> "
            + text.replace(". ", ". <br/> ")
        )
        for keyword in keywords:
            ptn = Keyword(KeywordCategory.ML_TOPIC, keyword, keyword, True).get_keyword_ptn()
            html_text = ptn.sub(rf" \g<PREK><span class='{highlight_class}'>\g<KEYWORD></span>\g<POSTK> ", html_text)
        html_text += " </div>"
        return HTML(html_text)

    def get_keyword_ptn(self) -> re.Pattern:
        _keyword = self.word.lower().replace("-", r"(\-|\s)*").replace(" ", r"(\s|\-)*")
        return re.compile(
            rf"""(?P<PREK>(^|\s|\(|'|")+)(?P<KEYWORD>{_keyword}(s|ing|al|d|ed|\-[^\s]+)*)(?P<POSTK>($|\s|\.|,|:|;|\)|'|")+)""",
            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )

    @staticmethod
    def get_ptn(text) -> re.Pattern:
        _keyword = text.lower().replace("-", r"(\-|\s)*").replace(" ", r"(\s|\-)*")
        return re.compile(
            rf"""(?P<PREK>(^|\s|\(|'|")+)(?P<KEYWORD>{_keyword}(s|ing|al|d|ed|\-[^\s]+)*)(?P<POSTK>($|\s|\.|,|:|;|\)|'|")+)""",
            flags=re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category.value,
            "word": self.word,
            "alias": self.alias,
        }


class MeCabPos(Enum):
    NOUN = "名詞"
    NOUN_GENERAL = "一般"
    NOUN_NAMED_ENTITY = "固有名詞"
    NOUN_NUMBER = "数"


@dataclass
class MeCabItem(object):
    word: str
    tag: MeCabPos = MeCabPos.NOUN
    pos1: MeCabPos = MeCabPos.NOUN_GENERAL
    pos2: str = "*"
    pos3: str = "*"
    cost: int = 10

    def to_list(self) -> list[str]:
        kks = pykakasi.kakasi()
        kana = "".join([token["kana"] for token in kks.convert(self.word)])
        return [
            self.word.strip(),
            "*",
            "*",
            str(self.cost),
            self.tag.value,
            self.pos1.value,
            self.pos2,
            self.pos3,
            "*",
            "*",
            self.word.strip(),
            kana,
            kana,
        ]


def extract_keywords(
    text: str, keywords: list[Keyword], remove_stopwords: bool = False, target_lang: str = "en"
) -> list[Keyword]:
    extracted = []

    if target_lang == "en":
        pass
    elif target_lang == "ja":
        tokenizer = MeCab.Tagger(f"-d {ipadic.DICDIR} -u {USER_DIC} -Owakati")
        tokens = [t.strip() for t in tokenizer.parse(text).split()]
        tokens = list(set([t.lower() for t in tokens if len(t) > 0]))
        text = " ".join(tokens)
    else:
        raise ValueError(f"Unsupported language: {target_lang}")

    for kw in keywords:
        if remove_stopwords and kw.score <= 1:
            continue
        ptn = kw.get_keyword_ptn()
        for m in ptn.finditer(text):
            extracted.append((m.start(), m.end(), kw))
    extracted = sorted(extracted, key=lambda x: x[0])
    return [kw for _, _, kw in extracted]


def add_noun_to_mecab_dict(items: list[MeCabItem], user_dic: Path = Path(USER_DIC), logger: Optional[Logger] = None):
    """add a new word to MeCab user dictionary

    Args:
        items (List[MeCabItem]): MeCabItems to add to the dictionary.
    """
    words: dict[str, list[str]] = {}

    # check the dictionary if the word is already added
    if TEMP_DICT_CSV.exists():
        with open(TEMP_DICT_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            words = {line[0]: line for line in reader}

            if logger:
                logger.info(f"Loaded {len(words)} words from the user dictionary")
            else:
                print(f"Loaded {len(words)} words from the user dictionary")

    # register new word
    for item in tqdm(items, desc="Adding new words to the dictionary", leave=False):
        if item.word in words:
            if item.pos2 != "*":
                words[item.word][6] = item.pos2
            if item.pos3 != "*":
                words[item.word][7] = item.pos3
            if item.cost != 10:
                words[item.word][3] = str(item.cost)
        else:
            words[item.word] = item.to_list()

    # write into the user dictionary csv
    with open(TEMP_DICT_CSV, mode="w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(words.values())

    # update the mecab dictionary
    mecab_dict_index_list = [Path(f) for f in glob("/usr/lib*/**/mecab-dict-index", recursive=True)]
    assert len(mecab_dict_index_list) > 0, "No MeCab dictionary index found"
    mecab_dict_index = mecab_dict_index_list[0]

    if logger:
        logger.info(f"Using MeCab dictionary index: {mecab_dict_index}")
    else:
        print(f"Using MeCab dictionary index: {mecab_dict_index}")

    Path(user_dic).parent.mkdir(exist_ok=True, parents=True)

    cmd = (
        f"{str(mecab_dict_index.absolute())} "
        + f"-d {ipadic.DICDIR} "
        + f"-u {str(user_dic)} -f utf-8 -t utf-8 {str(TEMP_DICT_CSV)}"
    )
    subprocess.run(cmd, shell=True)

    if logger:
        logger.info(f"Added {len(words)} words to the user dictionary")
        logger.info(f"compiled user dictionary -> {user_dic}")
    else:
        print(f"compiled user dictionary -> {user_dic}")


def add_keywords_to_mecab_dic(keywords: list[Keyword]):
    items = [MeCabItem(w.keyword) for w in keywords]
    add_noun_to_mecab_dict(items)
