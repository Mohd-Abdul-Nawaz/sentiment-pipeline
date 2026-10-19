# Real-Time Sentiment Analysis Pipeline

A Kafka-based streaming pipeline for real-time sentiment analysis with FastAPI backend — part of the Enterpret Backend SDE Intern portfolio.

## 🏗️ Architecture

```
Text Input → Kafka Topic → Consumer → NLP Analysis → API → Results
```

- **Producer**: Simulates real-time feedback ingestion into Kafka
- **Consumer**: Reads from Kafka, runs sentiment analysis, stores results
- **API**: FastAPI backend serving analysis results with filtering and stats

## 🚀 Quick Start

### Docker (Full Stack)
```bash
docker-compose up --build
```
- API: `http://localhost:8000/docs`
- Kafka: `localhost:9092`

### Local Python (API Only)
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 API Endpoints

### Analyze Text
```http
POST /api/analyze
Content-Type: application/json

{
  "text": "I love this product!",
  "source": "mobile_app"
}
```

**Response:**
```json
{
  "id": "uuid",
  "text": "I love this product!",
  "source": "mobile_app",
  "sentiment": "positive",
  "confidence_score": 0.85,
  "keywords": ["love", "product"],
  "created_at": "2024-01-15T10:30:00"
}
```

### Get Results
```http
GET /api/results?sentiment=positive&limit=10
```

### Get Stats
```http
GET /api/stats
```

## ☁️ Deploy to AWS

### EC2 / ECS with Docker
```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.ap-south-1.amazonaws.com
docker build -t sentiment-pipeline .
docker tag sentiment-pipeline:latest <account>.dkr.ecr.ap-south-1.amazonaws.com/sentiment-pipeline:latest
docker push <account>.dkr.ecr.ap-south-1.amazonaws.com/sentiment-pipeline:latest
```

### Managed Streaming for Kafka (MSK)
Replace self-hosted Kafka with AWS MSK for production.

### Lambda for Consumer
Deploy consumer.py as a Lambda function triggered by MSK events.

## 🧠 NLP Processing

- Sentiment: Positive / Negative / Neutral (keyword-based scoring)
- Keyword extraction: Top 5 meaningful words per text
- Extensible: Swap `app/nlp.py` with transformer models (DistilBERT, RoBERTa)

## 🧪 Run Tests
```bash
pytest tests/ -v
```

## 🔧 Make Commands
| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make run` | Start FastAPI server |
| `make up` | Start full Docker stack |
| `make test` | Run tests |
| `make producer` | Run Kafka producer |
| `make consumer` | Run Kafka consumer |

---
**Built for Enterpret Backend SDE Intern application.**