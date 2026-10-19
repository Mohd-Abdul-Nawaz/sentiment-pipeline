from app.nlp import analyze
from app.models import SentimentLabel


def test_analyze_positive():
    result = analyze("I love this amazing app!")
    assert result["sentiment"] == SentimentLabel.POSITIVE
    assert result["confidence_score"] > 0.5
    assert len(result["keywords"]) > 0


def test_analyze_negative():
    result = analyze("This is terrible and broken.")
    assert result["sentiment"] == SentimentLabel.NEGATIVE
    assert result["confidence_score"] > 0.5


def test_analyze_neutral():
    result = analyze("It is okay, nothing special.")
    assert result["sentiment"] in [SentimentLabel.NEUTRAL, SentimentLabel.POSITIVE]


def test_extract_keywords():
    result = analyze("The login button is broken and slow")
    assert isinstance(result["keywords"], list)
    assert len(result["keywords"]) > 0