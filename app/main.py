from fastapi import FastAPI
from app.routes import sentiment, health

app = FastAPI(
    title="Real-Time Sentiment Analysis Pipeline",
    description="Kafka-based streaming pipeline for real-time sentiment analysis with FastAPI backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(sentiment.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Real-Time Sentiment Analysis Pipeline",
        "docs": "/docs",
        "health": "/api/health",
    }