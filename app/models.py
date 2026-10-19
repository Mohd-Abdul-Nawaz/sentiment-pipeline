from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to analyze")
    source: Optional[str] = Field(None, description="Source of the text")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class SentimentResult(BaseModel):
    id: str
    text: str
    source: Optional[str]
    sentiment: SentimentLabel
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    keywords: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class StreamMessage(BaseModel):
    text: str
    source: Optional[str]
    timestamp: str