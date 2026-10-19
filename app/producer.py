"""
Kafka producer for streaming text data into the sentiment pipeline.
Run this to simulate real-time data ingestion.
"""

import json
import time
import random
from kafka import KafkaProducer

SAMPLE_TEXTS = [
    "I love this product! It's amazing.",
    "The app is terrible and keeps crashing.",
    "It's okay, nothing special but works fine.",
    "Best purchase I've made this year!",
    "Worst customer service ever.",
    "The new feature is great and helpful.",
    "I'm disappointed with the quality.",
    "Fast delivery and excellent packaging.",
    "Not worth the price.",
    "Absolutely fantastic experience!",
]

SAMPLE_SOURCES = ["mobile_app", "web", "email", "survey", "social_media"]


def produce_messages(bootstrap_servers: str = "localhost:9092", topic: str = "raw-feedback"):
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    print(f"Producing messages to Kafka topic: {topic}")
    try:
        while True:
            text = random.choice(SAMPLE_TEXTS)
            source = random.choice(SAMPLE_SOURCES)
            message = {
                "text": text,
                "source": source,
                "timestamp": time.time(),
            }
            producer.send(topic, value=message)
            print(f"Sent: {text[:50]}... (source: {source})")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.close()


if __name__ == "__main__":
    produce_messages()