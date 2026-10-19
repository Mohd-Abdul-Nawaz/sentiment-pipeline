from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.models import TextInput, SentimentResult, SentimentLabel
from app.nlp import analyze
import uuid
from datetime import datetime

router = APIRouter(tags=["sentiment"])

# In-memory store for demo (replace with PostgreSQL/Redis in production)
_results: List[SentimentResult] = []


@router.post("/analyze", response_model=SentimentResult, status_code=201)
async def analyze_text(input: TextInput):
    """Analyze sentiment of a single text input."""
    result = analyze(input.text)

    sentiment_result = SentimentResult(
        id=str(uuid.uuid4()),
        text=input.text,
        source=input.source,
        sentiment=result["sentiment"],
        confidence_score=result["confidence_score"],
        keywords=result["keywords"],
        created_at=datetime.utcnow(),
    )

    _results.append(sentiment_result)
    return sentiment_result


@router.get("/results", response_model=List[SentimentResult])
async def get_results(
    sentiment: Optional[SentimentLabel] = Query(None, description="Filter by sentiment"),
    limit: int = Query(50, ge=1, le=100, description="Max items to return"),
):
    """Get sentiment analysis results with optional filtering."""
    filtered = _results
    if sentiment:
        filtered = [r for r in filtered if r.sentiment == sentiment]
    return filtered[-limit:]


@router.get("/results/{result_id}", response_model=SentimentResult)
async def get_result(result_id: str):
    """Get a single sentiment result by ID."""
    for r in _results:
        if r.id == result_id:
            return r
    raise HTTPException(status_code=404, detail="Result not found")


@router.get("/stats")
async def get_stats():
    """Get aggregate sentiment statistics."""
    total = len(_results)
    if total == 0:
        return {"total": 0, "positive": 0, "negative": 0, "neutral": 0}

    pos = sum(1 for r in _results if r.sentiment == SentimentLabel.POSITIVE)
    neg = sum(1 for r in _results if r.sentiment == SentimentLabel.NEGATIVE)
    neu = sum(1 for r in _results if r.sentiment == SentimentLabel.NEUTRAL)

    return {
        "total": total,
        "positive": pos,
        "negative": neg,
        "neutral": neu,
        "positive_pct": round(pos / total * 100, 2),
        "negative_pct": round(neg / total * 100, 2),
        "neutral_pct": round(neu / total * 100, 2),
    }