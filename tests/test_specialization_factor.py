from keywords.keywords import Keyword, KeywordCategory
from keywords.metrics import SpecializationFactor


def test_calculate():
    input_text = [
        "a b c NER d e f g NER h i j NER.",
        "a b c NER d e f g NER h i j NER.",
        "a b c NER d e f g NER h i j NER.",
        "a b c NER d e f g NER h i j NER.",
        "a b c NER d e f g NER h i j NER.",
        "a b c MT d e f g MT h i j MT a NER a NER a NER.",
    ]

    factors = SpecializationFactor.calculate(input_text)

    assert factors.loc[0, "Named Entity Recognition"] > 1.0
    assert factors.loc[5, "Named Entity Recognition"] < 1.0
    assert factors.loc[5, "Neural Machine Translation"] > 1.0
