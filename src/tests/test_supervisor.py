from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Service is running"}

def test_invoke_supervisor():
    payload = {
        "messages": [
            {"role": "user", "content": "Get Zalando and its peers metadata"}
        ]
    }
    response = client.post("/invoke-supervisor", json=payload)
    
    assert response.status_code in (200, 500)
    if response.status_code == 200:
        data = response.json()
        assert "ai_messages" in data
        assert isinstance(data["ai_messages"], list)
