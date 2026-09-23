from fastapi.testclient import TestClient

from app import app
from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Loan Approval Prediction API"
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_predict():
    payload = {
        "loan_amount": 15000,
        "risk_score": 720,
        "dti": 18.5,
        "employment_years": 5,
        "application_year": 2018,
        "application_month": 6,
        "application_quarter": 2,
        "purpose": "debt_consolidation",
        "state": "CA"
    }

    response = client.post(
        "/predict",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] == 1
    assert data["decision"] == "Accepted"

    assert (
        0.0
        <= data["approval_probability"]
        <= 1.0
    )