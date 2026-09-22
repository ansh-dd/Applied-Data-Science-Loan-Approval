# Experiment 6 - Containerization & API Deployment

## Aim
Containerization and API Deployment.

## Objective
Package the trained loan approval model in Docker and expose predictions through FastAPI.

## API Endpoints

### GET /
Checks whether the API is running.

### GET /health
Checks API and model availability.

### POST /predict
Predicts whether a loan application is Accepted or Rejected.

## Example Request

{
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

## Docker Build

docker build -t loan-approval-api .

## Docker Run

docker run -d -p 8000:8000 --name loan-api loan-approval-api

## Health Endpoint

http://localhost:8000/health

## Swagger Documentation

http://localhost:8000/docs

## Automated Windows Test

powershell -ExecutionPolicy Bypass -File docker_test.ps1