"""
Sentiment analysis module using lightweight keyword-based scoring.
Can be extended with transformers (DistilBERT, RoBERTa) for production.
"""

import re
from typing import Tuple, List
from app.models import SentimentLabel


POSITIVE_WORDS = {
    "good", "great", "awesome", "amazing", "excellent", "fantastic", "best",
    "love", "loved", "like", "liked", "helpful", "wonderful", "perfect",
    "outstanding", "satisfied", "happy", "pleased", "thank", "thanks",
    "recommend", "impressive", "smooth", "fast", "easy", "intuitive",
    "brilliant", "superb", "exceptional", "remarkable", "stellar"
}

NEGATIVE_WORDS = {
    "bad", "terrible", "worst", "horrible", "awful", "poor", "disappointing",
    "frustrated", "frustrating", "annoyed", "annoying", "unhappy", "dissatisfied",
    "hate", "hated", "dislike", "disliked", "broken", "bug", "error", "slow",
    "expensive", "overpriced", "waste", "useless", "confusing", "difficult",
    "annoying", "problem", "issue", "fail", "failure", "crash"
}

NEUTRAL_WORDS = {
    "okay", "fine", "average", "normal", "standard", "decent", "acceptable",
    "mediocre", "fair", "moderate"
}


def analyze_sentiment(text: str) -> Tuple[SentimentLabel, float]:
    """Analyze sentiment and return label with confidence score."""
    text_lower = text.lower()

    pos_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    neg_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    neu_count = sum(1 for word in NEUTRAL_WORDS if word in text_lower)

    total = pos_count + neg_count + neu_count

    if total == 0:
        return SentimentLabel.NEUTRAL, 0.5

    if pos_count > neg_count:
        confidence = min(0.5 + (pos_count - neg_count) * 0.12, 0.95)
        return SentimentLabel.POSITIVE, round(confidence, 2)
    elif neg_count > pos_count:
        confidence = min(0.5 + (neg_count - pos_count) * 0.12, 0.95)
        return SentimentLabel.NEGATIVE, round(confidence, 2)
    else:
        return SentimentLabel.NEUTRAL, 0.5


def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """Extract meaningful keywords from text."""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "can", "this", "that", "these", "those",
        "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"
    }

    words = re.findall(r"\b\w+\b", text.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    from collections import Counter
    freq = Counter(keywords)
    return [word for word, _ in freq.most_common(max_keywords)]


def analyze(text: str) -> dict:
    """Full sentiment analysis: label + confidence + keywords."""
    sentiment, confidence = analyze_sentiment(text)
    keywords = extract_keywords(text)
    return {
        "sentiment": sentiment,
        "confidence_score": confidence,
        "keywords": keywords,
    }