from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_endpoint():
    response = client.post("/api/analyze", json={
        "text": "I love this product!",
        "source": "web"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["sentiment"] == "positive"
    assert 0.0 <= data["confidence_score"] <= 1.0


def test_get_results():
    client.post("/api/analyze", json={"text": "Great experience!"})
    response = client.get("/api/results")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_stats():
    client.post("/api/analyze", json={"text": "Amazing!"})
    response = client.get("/api/stats")
    assert response.status_code == 200
    assert "total" in response.json()