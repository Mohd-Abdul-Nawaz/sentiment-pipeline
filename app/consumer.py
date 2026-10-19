"""
Kafka consumer that reads raw feedback and runs sentiment analysis.
Results are stored for API retrieval.
"""

import json
import time
from kafka import KafkaConsumer
from app.nlp import analyze
import uuid
from datetime import datetime

# In-memory store (replace with DB in production)
results = []


def consume_messages(bootstrap_servers: str = "localhost:9092", topic: str = "raw-feedback"):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="sentiment-analyzer",
    )

    print(f"Consuming from Kafka topic: {topic}")
    try:
        for message in consumer:
            data = message.value
            text = data.get("text", "")
            source = data.get("source")

            result = analyze(text)

            sentiment_result = {
                "id": str(uuid.uuid4()),
                "text": text,
                "source": source,
                "sentiment": result["sentiment"],
                "confidence_score": result["confidence_score"],
                "keywords": result["keywords"],
                "created_at": datetime.utcnow().isoformat(),
            }

            results.append(sentiment_result)
            print(f"Analyzed: {text[:50]}... -> {result['sentiment']} ({result['confidence_score']})")

            # Keep only last 1000 results in memory
            if len(results) > 1000:
                results.pop(0)
    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    consume_messages()