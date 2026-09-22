
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Load trained model
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR /
    "best_loan_approval_model.joblib"
)

model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Loan Approval Prediction API",
    description=(
        "API for predicting loan application approval "
        "using the trained Experiment 4 machine learning model."
    ),
    version="1.0.0"
)


# ---------------------------------------------------------
# Input schema
# ---------------------------------------------------------

class LoanApplication(BaseModel):

    loan_amount: float = Field(
        ...,
        gt=0
    )

    risk_score: float | None = None

    dti: float | None = None

    employment_years: float | None = None

    application_year: int

    application_month: int = Field(
        ...,
        ge=1,
        le=12
    )

    application_quarter: int = Field(
        ...,
        ge=1,
        le=4
    )

    purpose: str

    state: str


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Loan Approval Prediction API",
        "status": "running"
    }


# ---------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True
    }


# ---------------------------------------------------------
# Prediction endpoint
# ---------------------------------------------------------

@app.post("/predict")
def predict(application: LoanApplication):

    try:

        input_df = pd.DataFrame([
            application.model_dump()
        ])

        prediction = int(
            model.predict(
                input_df
            )[0]
        )

        probability = float(
            model.predict_proba(
                input_df
            )[0][1]
        )

        decision = (
            "Accepted"
            if prediction == 1
            else "Rejected"
        )

        return {
            "prediction": prediction,
            "decision": decision,
            "approval_probability": round(
                probability,
                4
            )
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
