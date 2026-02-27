$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\\.venv")) {
  python -m venv .venv
}

.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt

python -m uvicorn bewise_app.main:app --host 0.0.0.0 --port 8000

