import random

from keywords.keywords import Keyword, KeywordCategory


def test_load_keywords():
    keywords = Keyword.load_keywords()
    assert len(keywords) > 0


def test_keyword_reg_ptn():
    keywords = [
        Keyword(KeywordCategory.CV_MODEL, "keyword"),
        Keyword(KeywordCategory.CV_MODEL, "key word"),
        Keyword(KeywordCategory.CV_MODEL, "key-word"),
        Keyword(KeywordCategory.CV_MODEL, "k e y w o r d"),
    ]

    for keyword in keywords:
        ptn = keyword.get_keyword_ptn()
        assert len(ptn.findall(f"{keyword.keyword}")) > 0
        assert len(ptn.findall(f"{keyword.keyword.replace('-', ' ')}")) > 0
        assert len(ptn.findall(f"{keyword.keyword.replace('-', '')}")) > 0
        assert len(ptn.findall(f"{keyword.keyword.replace(' ', '-')}")) > 0
        assert len(ptn.findall(f"{keyword.keyword}.")) > 0
        assert len(ptn.findall(f"test {keyword.keyword} test.")) > 0
        assert len(ptn.findall(f"test {keyword.keyword}s")) > 0
        assert len(ptn.findall(f"test {keyword.keyword}ing")) > 0
        assert len(ptn.findall(f"test {keyword.keyword}al")) > 0
        assert len(ptn.findall(f"test {keyword.keyword},")) > 0
        assert len(ptn.findall(f"test {keyword.keyword}.")) > 0
        assert len(ptn.findall(f"test {keyword.keyword}:")) > 0
        assert len(ptn.findall(f"test {keyword.keyword};")) > 0
        assert len(ptn.findall(f"({keyword.keyword})")) > 0
        assert (
            ptn.sub(r"\g<PREK><span>\g<KEYWORD></span>\g<POSTK>", keyword.keyword) == f"<span>{keyword.keyword}</span>"
        )
        assert (
            ptn.sub(r"\g<PREK><span>\g<KEYWORD></span>\g<POSTK>", f"({keyword.keyword})")
            == f"(<span>{keyword.keyword}</span>)"
        )
