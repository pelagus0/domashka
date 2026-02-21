$ErrorActionPreference = "Stop"

python -m pip install -r requirements-dev.txt
python -m isort .
python -m flake8 .

