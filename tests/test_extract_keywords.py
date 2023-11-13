from keywords.keywords import Keyword, KeywordCategory, extract_keywords


def test_extract_keywords():
    text = "This is a test sentence with the keyword 'test' in it."
    keywords = [Keyword(KeywordCategory.OTHER, "test", "test", True)]
    extracted_keywords = extract_keywords(text, keywords)
    assert isinstance(extracted_keywords, list)
    assert len(extracted_keywords) == 2
    assert extracted_keywords[1].keyword == "test"
    assert extracted_keywords[1].category == KeywordCategory.OTHER


def test_extract_keywords_with_remove_stopwords():
    text = "This is a test sentence with the keyword 'test' in it."
    keywords = [
        Keyword(KeywordCategory.OTHER, "test", "test", True, 1),
        Keyword(KeywordCategory.NLP_TOPIC, "sentence", "sentence", True, 10),
    ]
    extracted_keywords = extract_keywords(text, keywords, remove_stopwords=True)
    assert isinstance(extracted_keywords, list)
    assert len(extracted_keywords) == 1
    assert extracted_keywords[0].keyword == "sentence"
    assert extracted_keywords[0].category == KeywordCategory.NLP_TOPIC
