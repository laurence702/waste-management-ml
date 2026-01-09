from fastapi.testclient import TestClient
from app.models import Area, WasteLog, WasteType

def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to EcoOps Waste Management API"}

def test_create_area(client: TestClient):
    response = client.post(
        "/areas/",
        json={"name": "Downtown", "code": "DT-001", "description": "City center"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Downtown"
    assert data["code"] == "DT-001"
    assert data["id"] is not None

def test_create_duplicate_area(client: TestClient):
    client.post(
        "/areas/",
        json={"name": "Uptown", "code": "UP-001"},
    )
    response = client.post(
        "/areas/",
        json={"name": "Uptown", "code": "UP-001"},
    )
    assert response.status_code == 400

def test_create_log(client: TestClient):
    area_resp = client.post(
        "/areas/",
        json={"name": "Industrial", "code": "IND-001"},
    )
    area_id = area_resp.json()["id"]

    response = client.post(
        "/logs/",
        json={
            "area_id": area_id,
            "waste_type": "general",
            "weight_kg": 150.5,
            "truck_id": "T-99"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["weight_kg"] == 150.5
    assert data["waste_type"] == "general"

def test_create_log_negative_weight(client: TestClient):
    # Create area first
    area_resp = client.post("/areas/", json={"name": "Test2", "code": "T-2"})
    area_id = area_resp.json()["id"]
    
    response = client.post(
        "/logs/",
        json={
            "area_id": area_id,
            "waste_type": "general",
            "weight_kg": -10.0,
        },
    )
    assert response.status_code == 400
    assert "Weight cannot be negative" in response.json()["detail"]
