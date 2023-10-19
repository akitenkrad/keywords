from keywords.keywords import Keyword, KeywordCategory
from keywords.metrics import TfIdf


def test_calculate():
    input_text = [
        "a b c NER d e f g NER h i j NER.",
        "a b c NER d e f g NER h i j NER.",
        "a b c NER d e f g NER h i j NER.",
        "a b c NER d e f g NER h i j NER.",
        "a b c NER d e f g NER h i j NER.",
        "a b c MT d e f g MT h i j MT a NER a NER a NER.",
    ]

    scores = TfIdf.calculate(input_text)

    assert scores.loc[0, "Named Entity Recognition"] > scores.loc[0, "Machine Translation"]
    assert scores.loc[5, "Named Entity Recognition"] < scores.loc[5, "Machine Translation"]
