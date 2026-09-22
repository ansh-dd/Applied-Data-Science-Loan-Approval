
Write-Host "=============================================="
Write-Host "ADS EXPERIMENT 6 - DOCKER LOCAL TEST"
Write-Host "=============================================="

Write-Host "`n[1] Building Docker image..."
docker build -t loan-approval-api .

if ($LASTEXITCODE -ne 0) {
    Write-Host "DOCKER BUILD FAILED"
    exit 1
}

docker rm -f loan-api 2>$null

Write-Host "`n[2] Starting Docker container..."
docker run -d -p 8000:8000 --name loan-api loan-approval-api

if ($LASTEXITCODE -ne 0) {
    Write-Host "DOCKER RUN FAILED"
    exit 1
}

Write-Host "`nWaiting for API..."
Start-Sleep -Seconds 8

Write-Host "`n[3] Running container:"
docker ps

Write-Host "`n[4] Testing /health..."

$health = Invoke-RestMethod `
    -Uri "http://localhost:8000/health" `
    -Method GET

$health | ConvertTo-Json

Write-Host "`n[5] Testing /predict..."

$body = @{
    loan_amount = 15000
    risk_score = 720
    dti = 18.5
    employment_years = 5
    application_year = 2018
    application_month = 6
    application_quarter = 2
    purpose = "debt_consolidation"
    state = "CA"
} | ConvertTo-Json

$prediction = Invoke-RestMethod `
    -Uri "http://localhost:8000/predict" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$prediction | ConvertTo-Json

Write-Host "`n=============================================="
Write-Host "DOCKER CONTAINER TEST PASSED"
Write-Host "=============================================="

Write-Host "`nStopping container..."
docker stop loan-api
docker rm loan-api
