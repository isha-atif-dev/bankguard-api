import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_transaction():
    payload = {
        "amount": 150.00,
        "currency": "GBP",
        "merchant_name": "Barclays Bank",
        "description": "Monthly subscription payment"
    }
    response = client.post("/api/v1/transactions/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 150.00
    assert data["currency"] == "GBP"
    assert data["merchant_name"] == "Barclays Bank"
    assert data["status"] == "pending"
    assert "id" in data


def test_create_transaction_invalid_amount():
    payload = {
        "amount": -50,
        "currency": "GBP",
        "merchant_name": "Barclays Bank"
    }
    response = client.post("/api/v1/transactions/", json=payload)
    assert response.status_code == 422


def test_get_transaction():
    payload = {
        "amount": 200.00,
        "currency": "USD",
        "merchant_name": "HSBC",
        "description": "Wire transfer"
    }
    create_response = client.post("/api/v1/transactions/", json=payload)
    transaction_id = create_response.json()["id"]

    response = client.get(f"/api/v1/transactions/{transaction_id}")
    assert response.status_code == 200
    assert response.json()["id"] == transaction_id


def test_get_transaction_not_found():
    response = client.get("/api/v1/transactions/invalid-id-999")
    assert response.status_code == 404


def test_update_transaction_status():
    payload = {
        "amount": 75.00,
        "currency": "EUR",
        "merchant_name": "Lloyds Bank"
    }
    create_response = client.post("/api/v1/transactions/", json=payload)
    transaction_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/transactions/{transaction_id}/status",
        json={"status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_transaction():
    payload = {
        "amount": 300.00,
        "currency": "GBP",
        "merchant_name": "NatWest"
    }
    create_response = client.post("/api/v1/transactions/", json=payload)
    transaction_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/transactions/{transaction_id}")
    assert response.status_code == 200

    get_response = client.get(f"/api/v1/transactions/{transaction_id}")
    assert get_response.status_code == 404